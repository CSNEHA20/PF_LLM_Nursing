import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Workspace from './pages/Workspace';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/" element={<Workspace />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
