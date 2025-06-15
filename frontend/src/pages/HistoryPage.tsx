import {useEffect, useRef, useState} from "react";
import {getAnalysisHistory} from "../api";

export const HistoryPage = () => {
    const [history, setHistory] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchedOnce = useRef(false);

    useEffect(() => {
        if (fetchedOnce.current) return;
        fetchedOnce.current = true;
        getAnalysisHistory().then((data) => {
            setHistory(data);
            setLoading(false);
        });
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Analysis History</h1>

            {loading ? (
                <p>Loading history...</p>
            ) : history.length === 0 ? (
                <p>No analysis history found.</p>
            ) : (
                <div className="space-y-4">
                    {history.map((item) => (
                        <div
                            key={item.id}
                            className="border rounded p-4 bg-white shadow-sm space-y-2"
                        >
                            <div className="text-sm text-gray-600">
                                <span className="font-medium">Date:</span>{" "}
                                {new Date(item.created_at).toLocaleString()}<br/>
                                <span className="font-medium">Document:</span>{" "}
                                {item.document?.filename || "N/A"} <br/>
                                <span className="font-medium">Prompt:</span>{" "}
                                {item.prompt_template?.name || "Custom"} <br/>
                                <details className="bg-gray-100 p-2 rounded mt-2 text-sm whitespace-pre-wrap">
                                    <summary className="cursor-pointer font-semibold">
                                        Final Prompt
                                    </summary>
                                    <div>{item.final_prompt}</div>
                                </details>

                            </div>

                            <details className="bg-gray-100 p-2 rounded mt-2 text-sm whitespace-pre-wrap">
                                <summary className="cursor-pointer font-semibold">
                                    AI Response
                                </summary>
                                <div>{item.gemini_response || "No response available."}</div>
                            </details>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};
