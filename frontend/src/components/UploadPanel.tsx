import {useState} from "react";
import {uploadFile, listenToProgress} from "../api";

export const UploadPanel = ({onUploadComplete}: { onUploadComplete: (id: string) => void }) => {
    const [file, setFile] = useState<File | null>(null);
    const [progress, setProgress] = useState<number>(0);
    const [stage, setStage] = useState<string>("");

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const f = e.target.files?.[0];
        if (!f) return;
        if (!["application/pdf", "text/plain"].includes(f.type)) {
            alert("Only PDF or TXT allowed");
            return;
        }
        if (f.size > 5 * 1024 * 1024) {
            alert("Max 5MB allowed");
            return;
        }
        setFile(f);
    };

    const handleUpload = async () => {
        if (!file) return;
        const {file_id} = await uploadFile(file);
        listenToProgress(
            file_id,
            ({progress, current_stage}) => {
                setProgress(progress);
                setStage(current_stage);
                if (progress === 100) onUploadComplete(file_id);
            },
            (err) => {
                console.error(err);
            }
        );
    };

    return (
        <div className="border p-6 rounded-lg bg-white shadow-md space-y-4 max-w-xl">
            <h2 className="text-lg font-bold">Upload Document</h2>
            <input
                type="file"
                accept=".pdf,.txt"
                className="block w-full text-sm text-gray-700"
                onChange={handleFileChange}
            />
            {file && (
                <div className="text-sm text-gray-600">
                    <strong>Selected:</strong> {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </div>
            )}
            <button
                onClick={handleUpload}
                disabled={!file}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300"
            >
                Upload & Track
            </button>
            {stage && (
                <div>
                    <p className="text-sm text-gray-700 mb-1">
                        <strong>Stage:</strong> {stage}
                    </p>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                            className="bg-blue-500 h-3 rounded-full transition-all"
                            style={{width: `${progress}%`}}
                        ></div>
                    </div>
                </div>
            )}
        </div>
    );
};
