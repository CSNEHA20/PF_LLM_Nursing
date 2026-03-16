import React from 'react';
import { Sparkles } from 'lucide-react';

export default function SuggestedPrompts({ onSelectPrompt }) {
    const prompts = [
        "Explain drug classifications",
        "How IV drug administration works",
        "Patient safety protocol summary",
        "Pharmacy dosage calculation example"
    ];

    return (
        <div className="mb-6 animate-fade-in">
            <div className="flex items-center gap-2 mb-3 text-text_secondary px-2">
                <Sparkles size={16} className="text-primary" />
                <span className="text-sm font-medium">Suggested Learning Prompts</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {prompts.map((prompt, idx) => (
                    <button
                        key={idx}
                        onClick={() => onSelectPrompt(prompt)}
                        className="text-left p-3 rounded-xl border border-gray-100 bg-surface hover:border-primary hover:bg-primary/5 transition-colors text-sm text-text_primary shadow-sm"
                    >
                        {prompt}
                    </button>
                ))}
            </div>
        </div>
    );
}
