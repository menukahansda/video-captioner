import FileUploader from "./components/FileUploader";
import { useEffect } from "react";
import { getUserId } from "./utils/userId";
import "./App.css";

export default function App() {
  useEffect(() => {
    const userId = getUserId();

    const cleanup = () => {
      navigator.sendBeacon(`${import.meta.env.VITE_API_URL}/cleanup/${userId}`);
    };

    window.addEventListener("beforeunload", cleanup);

    return () => {
      window.removeEventListener("beforeunload", cleanup);
    };
  }, []);

  return (
    <main className="min-h-screen flex justify-center pt-12">
      <FileUploader />
    </main>
  );
}
