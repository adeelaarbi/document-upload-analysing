import Select from "react-select";
import {useEffect, useRef, useState} from "react";
import {PromptLibrary, type PromptTemplate} from "../components/PromptLibrary";
import {analyzeWithPrompt, getDocuments} from "../api";

export const AnalyzePage = () => {
    const [documents, setDocuments] = useState<any[]>([]);
    const [selectedDocId, setSelectedDocId] = useState<string | null>(null);
    const [selectedPrompt, setSelectedPrompt] = useState<PromptTemplate | null>(null);
    const [question, setQuestion] = useState("");
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState("");

    const fetchedOnce = useRef(false);

    useEffect(() => {
        if (fetchedOnce.current) return;
        fetchedOnce.current = true;

        getDocuments().then(setDocuments);
    }, []);

    const docOptions = documents.map((doc) => ({
        value: doc.id,
        label: `${doc.filename} (${doc.status})`,
    }));

    const handleAnalyze = async () => {
        if (!selectedPrompt || !selectedDocId || !question.trim()) return;

        setLoading(true);
        try {
            const result = await analyzeWithPrompt({
                document_id: selectedDocId,
                prompt_template_id: selectedPrompt.id,
                question,
            });
            setResponse(result.response_text || "No response received.");
        } catch (error: any) {
            setResponse("❌ Failed to analyze: " + (error?.message || "Unknown error"));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 space-y-6">
            <div>
                <label className="block font-medium mb-2">Select a Document</label>
                <Select
                    options={docOptions}
                    onChange={(option) => setSelectedDocId(option?.value || null)}
                    placeholder="Choose a document..."
                />
            </div>

            {!selectedPrompt && (
                <>
                    <h2 className="text-xl font-bold mb-4">Select a Prompt Template</h2>
                    <PromptLibrary onSelect={(prompt) => setSelectedPrompt(prompt)}/>
                </>
            )}

            {selectedPrompt && selectedDocId && (
                <div className="space-y-4">
                    <div className="bg-white p-4 border rounded shadow">
                        <h3 className="font-semibold mb-2">Template: {selectedPrompt.name}</h3>
                        <p className="text-sm text-gray-600">{selectedPrompt.description}</p>
                        <pre className="bg-gray-100 p-2 mt-2 rounded text-sm whitespace-pre-wrap">
                          {selectedPrompt.prompt_text}
                        </pre>
                    </div>

                    {
                        selectedPrompt.variables && selectedPrompt.variables.find(v => v.name === "question") && (
                            <div>
                                <label className="block font-medium mb-1">Question</label>
                                <input
                                    type="text"
                                    value={question}
                                    onChange={(e) => setQuestion(e.target.value)}
                                    placeholder="Ask something..."
                                    className="w-full border px-3 py-2 rounded"
                                />
                            </div>
                        )
                    }

                    <div className="flex items-center gap-4">
                        <button
                            onClick={handleAnalyze}
                            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                            disabled={loading}
                        >
                            {loading ? "Analyzing..." : "Run Analysis"}
                        </button>

                        <button
                            onClick={() => {
                                setSelectedDocId(null);
                                setSelectedPrompt(null);
                                setQuestion("Summarize the document");
                                setResponse("");
                                setLoading(false);
                            }}
                            className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
                        >
                            Reset
                        </button>
                    </div>


                    {response && (
                        <div className="mt-6">
                            <h3 className="text-lg font-semibold mb-1">AI Response</h3>
                            <pre className="bg-gray-100 p-3 rounded whitespace-pre-wrap text-sm">
                                {response}
                            </pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};
