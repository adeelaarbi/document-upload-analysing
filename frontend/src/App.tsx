// src/App.tsx
import {Link} from "react-router-dom";
import {AppRoutes} from "./routes";

export default function App() {
    return (
        <div className="min-h-screen bg-gray-50">
            <nav className="bg-white shadow p-4 mb-4 flex space-x-4">
                <Link to="/" className="text-blue-600 font-semibold">Upload</Link>
                <Link to="/analyze" className="text-blue-600 font-semibold">Analysis</Link>
                <Link to="/history" className="text-blue-600 font-semibold">History</Link>
            </nav>
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <AppRoutes/>
            </div>
        </div>
    );
}
