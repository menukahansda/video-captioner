import { useRef, useState, useEffect } from "react";
import { getUserId } from "../utils/userId";
import { LoaderCircle } from "lucide-react";

export default function FileUploader() {
  const fileInputRef = useRef(null);
  const [fileSelected, setFileSelected] = useState(false);
  const [isResult, setIsResult] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [previewFiles, setPreviewFiles] = useState([]);

  function formatStyleLabel(key) {
    return key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  }
  const handleSelectClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      setFileSelected(true);
      setPreviewFiles(
        Array.from(files).map((f) => ({
          stem: f.name.replace(/\.[^/.]+$/, ""),
          url: URL.createObjectURL(f),
        })),
      );
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
      const normalized = Object.entries(data.results ?? {}).map(
        ([taskId, value]) => ({
          taskId,
          summary: value.summary,
          captions: value.captions,
          previewUrl: previewFiles.find((p) =>
            taskId.startsWith(`${p.stem}_`),
          )?.url,
        }),
      );
      setResult(normalized);
      setIsResult(true);
    } catch (error) {
      console.error("Processing failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    return () => {
      previewFiles.forEach(({ url }) => URL.revokeObjectURL(url));
    };
  }, [previewFiles]);

  return (
    <div className="flex flex-col items-center gap-4">
      <button
        onClick={handleSelectClick}
        className="file-selector-btn"
        disabled={isLoading}
      >
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

      {isResult && result?.length > 0 && (
        <div className="results-container">
          {result.map((item) => (
            <div className="result-row" key={item.taskId}>
              <div className="result-video">
                {item.previewUrl && (
                  <video
                    src={item.previewUrl}
                    controls
                    preload="metadata"
                    className="result-video-el"
                  />
                )}
              </div>

              <div className="result-captions-grid">
                {Object.entries(item.captions ?? {}).map(([style, caption]) => (
                  <div className="caption-box" key={style}>
                    <h4 className="caption-style">{formatStyleLabel(style)}</h4>
                    <p className="caption-text">{caption}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
