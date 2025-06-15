// src/pages/UploadPage.tsx
import {useState} from "react";
import {UploadPanel} from "../components/UploadPanel";

export const UploadPage = () => {
    const [fileId, setFileId] = useState<string | null>(null);

    return (
        <div className="p-8">
            <h1 className="text-xl font-bold mb-4">Upload Document</h1>
            {!fileId ? (
                <UploadPanel onUploadComplete={setFileId}/>
            ) : (
                <p className="text-green-600">Upload complete. File ID: {fileId}</p>
            )}
        </div>
    );
};
