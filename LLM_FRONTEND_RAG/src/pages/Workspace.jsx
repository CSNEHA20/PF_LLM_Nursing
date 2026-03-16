import React from 'react';
import Sidebar from '../components/layout/Sidebar';
import TopBar from '../components/layout/TopBar';
import ChatPage from '../components/chat/ChatPage';

export default function Workspace() {
    return (
        <div className="flex h-screen w-full bg-background overflow-hidden relative text-text_primary">
            {/* Sidebar */}
            <Sidebar />

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col h-full overflow-hidden">
                <TopBar />
                <ChatPage />
            </div>
        </div>
    );
}
