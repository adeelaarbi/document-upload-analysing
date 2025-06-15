import {Route, Routes} from "react-router-dom";
import {UploadPage} from "../pages/UploadPage.tsx";
import {AnalyzePage} from "../pages/AnalyzePage.tsx";
import {HistoryPage} from "../pages/HistoryPage.tsx";

export function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<UploadPage/>}/>
            <Route path="/analyze" element={<AnalyzePage/>}/>
            <Route path="/history" element={<HistoryPage/>}/>
        </Routes>
    )
}