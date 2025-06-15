import {useEffect, useRef, useState} from "react";
import {getPromptTemplates} from "../api";

export interface PromptTemplate {
    id: string;
    name: string;
    description: string;
    category: string;
    prompt_text: string;
    variables?: Array<{ name: string; required: boolean }>
}

export const PromptLibrary = ({onSelect}: { onSelect: (prompt: PromptTemplate) => void }) => {
    const [prompts, setPrompts] = useState<PromptTemplate[]>([]);
    const fetchedOnce = useRef(false);

    useEffect(() => {
        if (fetchedOnce.current) return;
        fetchedOnce.current = true;
        getPromptTemplates().then(setPrompts);
    }, []);

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {prompts.map((prompt) => (
                <div key={prompt.id} className="bg-white p-4 rounded shadow-md border">
                    <h3 className="font-bold text-lg mb-1">{prompt.name}</h3>
                    <p className="text-sm text-gray-600 mb-2">{prompt.description}</p>
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full mb-2">
            {prompt.category}
          </span>
                    <button
                        className="block mt-2 text-sm text-blue-600 font-medium hover:underline"
                        onClick={() => onSelect(prompt)}
                    >
                        Use This Prompt
                    </button>
                </div>
            ))}
        </div>
    );
};
