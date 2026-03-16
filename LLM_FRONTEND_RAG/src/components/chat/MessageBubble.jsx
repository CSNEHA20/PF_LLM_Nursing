import React from 'react';
import { User, Sparkles } from 'lucide-react';
import { cn } from '../../utils/cn';

export default function MessageBubble({ message }) {
    const isUser = message.role === 'user';

    return (
        <div className={cn(
            "flex w-full",
            isUser ? "justify-end" : "justify-start"
        )}>
            <div className={cn(
                "flex max-w-[85%] sm:max-w-[75%] gap-4",
                isUser ? "flex-row-reverse" : "flex-row"
            )}>

                {/* Avatar */}
                <div className="flex-shrink-0 mt-1">
                    {isUser ? (
                        <div className="w-8 h-8 rounded-full bg-[#f0dae0] flex items-center justify-center text-[#b1103e] shadow-sm">
                            <User size={16} />
                        </div>
                    ) : (
                        <div className="w-8 h-8 rounded-full bg-[#b1103e] flex items-center justify-center text-white shadow-sm">
                            <Sparkles size={16} />
                        </div>
                    )}
                </div>

                {/* Message Content */}
                <div className={cn(
                    "px-5 py-3.5 rounded-2xl shadow-sm text-[15px] leading-relaxed",
                    isUser
                        ? "bg-[#b1103e] text-white rounded-tr-sm"
                        : "bg-[#e58ea8] border border-primary/10 text-[#111827] rounded-tl-sm"
                )}>
                    {/* Use pre-wrap to respect newlines but don't break simple markdown completely */}
                    <div className="whitespace-pre-wrap">
                        {message.content}
                    </div>
                </div>

            </div>
        </div>
    );
}
