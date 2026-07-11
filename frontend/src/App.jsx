import FileUploader from "./components/FileUploader";
import { useEffect, useState, useRef } from "react";
import { getUserId } from "./utils/userId";
import "./App.css";

const RETRY_INTERVAL_MS = 1000;
const MAX_RETRIES = 30;

export default function App() {
  const [serverStatus, setServerStatus] = useState("checking");
  const attemptsRef = useRef(0);

  useEffect(() => {
    const userId = getUserId();
    let cancelled = false;
    let timeoutId;

    const pingServer = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/`);
        if (cancelled) return;

        if (res.ok) {
          setServerStatus("ok");
          return; // stop polling
        }
        scheduleRetry();
      } catch {
        if (!cancelled) scheduleRetry();
      }
    };

    const scheduleRetry = () => {
      attemptsRef.current += 1;
      if (attemptsRef.current >= MAX_RETRIES) {
        if (!cancelled) setServerStatus("error");
        return;
      }
      timeoutId = setTimeout(pingServer, RETRY_INTERVAL_MS);
    };

    pingServer();

    const cleanup = () => {
      navigator.sendBeacon(`${import.meta.env.VITE_API_URL}/cleanup/${userId}`);
    };

    window.addEventListener("beforeunload", cleanup);

    return () => {
      cancelled = true;
      clearTimeout(timeoutId);
      window.removeEventListener("beforeunload", cleanup);
    };
  }, []);

  const handleRetry = () => {
    attemptsRef.current = 0;
    setServerStatus("checking");
    window.location.reload();
  };
  return (
    <main className="min-h-screen flex justify-center pt-12">
      {serverStatus === "checking" && (
        <p className="text-gray-500">Starting up, please wait...</p>
      )}

      {serverStatus === "error" && (
        <div className="text-center">
          <p className="text-red-500 font-medium">
            Unable to reach the server.
          </p>
          <button
            className="mt-3 px-4 py-2 rounded bg-gray-800 text-white"
            onClick={handleRetry}
          >
            Retry
          </button>
        </div>
      )}

      {serverStatus === "ok" && <FileUploader />}
    </main>
  );
}
