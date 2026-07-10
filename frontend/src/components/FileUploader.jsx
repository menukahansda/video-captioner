import { useRef, useState } from "react";
import { getUserId } from "../utils/userId";
import { LoaderCircle } from "lucide-react";

export default function FileUploader() {
  const fileInputRef = useRef(null);
  const [fileSelected, setFileSelected] = useState(false);
  const [isResult, setIsResult] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null); 

  const handleSelectClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      setFileSelected(true);
      console.log(
        "Selected files:",
        Array.from(files).map((f) => f.name),
      );
    }
  };

  const handleProcessClick = async () => {
    const files = fileInputRef.current.files;
    if (!files.length) return;

    const formData = new FormData();
    formData.append("userId", getUserId());
    Array.from(files).forEach((file) => {
      formData.append("videos", file);
    });

    setIsLoading(true);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/generate-captions`,
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      setIsResult(true);
    } catch (error) {
      console.error("Processing failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4">
      <button onClick={handleSelectClick} className="file-selector-btn" disabled={isLoading}>
        Select Videos
      </button>

      <input
        type="file"
        accept="video/*"
        ref={fileInputRef}
        onChange={handleFileChange}
        multiple
        hidden
      />

      {fileSelected && !isResult && (
        <button
          className="process-btn"
          onClick={handleProcessClick}
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <LoaderCircle className="spinner" size={20} />
              Processing...
            </>
          ) : (
            "Generate Captions"
          )}
        </button>
      )}

      {isResult && (
        <pre>
          {JSON.stringify(result, null, 2)}
        </pre> /* placeholder until UI is built */
      )}
    </div>
  );
}