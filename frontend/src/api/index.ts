import axios from "axios";

const API_BASE_URL = "http://localhost:8888/api";

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post(`/upload`, formData, {
        headers: {"Content-Type": "multipart/form-data"},
    });

    return response.data;
};

export const listenToProgress = (
    fileId: string,
    onMessage: (data: { progress: number; current_stage: string }) => void,
    onError: (error: any) => void
) => {
    const sse = new EventSource(`${API_BASE_URL}/stream/${fileId}`);
    sse.onmessage = (event) => {
        const parsed = JSON.parse(event.data);
        onMessage(parsed);
    };
    sse.onerror = (err) => {
        sse.close();
        onError(err);
    };
};

// Get prompt templates
export const getPromptTemplates = async () => {
    const response = await api.get("/prompt-templates");
    return response.data;
};

export const analyzeWithPrompt = async (data: {
    document_id: string;
    prompt_template_id: string;
    question?: string;
}) => {
    const {document_id, prompt_template_id, question} = data;
    const payload: {
        document_id: string;
        prompt_template_id: string;
        variables?: { question: string };
    } = {
        document_id,
        prompt_template_id
    };
    if (question) {
        payload.variables = { question }
    }
    const res = await api.post("/analyses", payload);
    return res.data;
};

export const getDocuments = async () => {
    const res = await api.get("/documents");
    return res.data; // List of { id, filename, upload_time, status }
};

export const getAnalysisHistory = async () => {
    const res = await api.get("/analyses/history");
    return res.data;
};



