import React from 'react';
import { User, Bell, ChevronDown } from 'lucide-react';

export default function TopBar() {
    return (
        <div className="h-[81px] flex-shrink-0 border-b border-black/10 bg-[#FFF5F5] flex items-center justify-between px-6 z-20 relative">
            <div className="flex flex-col flex-shrink-0">
                <div className="flex items-center gap-2 mb-0.5">
                    <span className="text-xs font-semibold text-text_primary/80 uppercase tracking-widest">Active Project</span>
                    <span className="text-[10px] bg-white/50 text-text_primary font-medium px-2 py-0.5 rounded-full border border-black/10">
                        RAG Learning Mode
                    </span>
                </div>
                <h2 className="text-[15px] font-semibold text-text_primary leading-tight">Pharmacology Basics</h2>
            </div>

            <div className="flex items-center gap-4 flex-shrink-0">
                <div className="flex items-center gap-2 cursor-pointer hover:bg-black/5 py-1.5 px-2 rounded-lg transition-colors border border-transparent hover:border-black/10">
                    <div className="w-8 h-8 rounded-full bg-[#FFD2D2] flex items-center justify-center text-[#F63939] border border-[#F63939]/30">
                        <User size={16} />
                    </div>
                    <span className="text-sm font-medium text-text_primary hidden sm:block">Sarah Connor</span>
                    <ChevronDown size={14} className="text-[#F63939]/80" />
                </div>
            </div>
        </div>
    );
}
