import React from 'react';
import { Book, Heart, Pill } from 'lucide-react';
import './DashboardArea.css';

export default function DashboardArea({ onNewLesson, onOpenProject, onOpenConcept }) {
    const projects = [
        { id: 1, title: "Drug Mechanisms", subtitle: "12 chats • last opened today", icon: Book, color: "text-blue-500", bg: "bg-blue-500/10" },
        { id: 2, title: "Nursing Fundamentals", subtitle: "8 chats • last opened yesterday", icon: Heart, color: "text-rose-500", bg: "bg-rose-500/10" },
        { id: 3, title: "Pharmacology Revision", subtitle: "15 chats • active project", icon: Pill, color: "text-purple-500", bg: "bg-purple-500/10" }
    ];

    const concepts = [
        "Antibiotics Overview",
        "IV Drug Administration",
        "Patient Safety Protocols",
        "Dosage Calculation Basics"
    ];

    const tags = [
        "Drug Classifications",
        "Nursing Ethics",
        "Emergency Drugs",
        "Pharmacy Calculations",
        "Clinical Case Learning"
    ];

    return (
        <div className="dashboard-container custom-scrollbar">
            {/* Welcome Header */}
            <div className="dashboard-header">
                <h1 className="dashboard-title">Welcome back, Student 👩‍⚕️</h1>
                <p className="dashboard-subtitle">Continue learning nursing and pharmacy concepts with AI guidance.</p>
            </div>

            {/* Action Row */}
            <div className="dashboard-action-row">
                <button
                    className="dashboard-btn-primary"
                    onClick={onNewLesson}
                >
                    + Start New Lesson
                </button>
                <button
                    className="dashboard-btn-secondary"
                    onClick={() => console.log('Explore Concepts clicked')}
                >
                    Explore Concepts
                </button>
            </div>

            {/* Learning Projects */}
            <div className="dashboard-section">
                <h2 className="dashboard-section-title">Your Learning Projects</h2>
                <div className="dashboard-card-grid">
                    {projects.map((project) => {
                        const Icon = project.icon;
                        return (
                            <div
                                key={project.id}
                                className="dashboard-project-card"
                                onClick={() => onOpenProject(project.id)}
                            >
                                <div className={`project-icon-wrapper ${project.bg} ${project.color}`}>
                                    <Icon size={24} />
                                </div>
                                <div className="project-info">
                                    <h3 className="project-title">{project.title}</h3>
                                    <p className="project-subtitle">{project.subtitle}</p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Recently Opened Concepts */}
            <div className="dashboard-section">
                <h2 className="dashboard-section-title">Recently Opened Concepts</h2>
                <div className="dashboard-horizontal-scroll">
                    {concepts.map((concept, index) => (
                        <div
                            key={index}
                            className="dashboard-concept-card"
                            onClick={() => onOpenConcept(concept)}
                        >
                            <span className="concept-text">{concept}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* AI Suggested Topics */}
            <div className="dashboard-section">
                <h2 className="dashboard-section-title">AI Suggested Topics</h2>
                <div className="dashboard-tag-list">
                    {tags.map((tag, index) => (
                        <span
                            key={index}
                            className="dashboard-tag"
                            onClick={() => console.log(`Tag clicked: ${tag}`)}
                        >
                            {tag}
                        </span>
                    ))}
                </div>
            </div>
        </div>
    );
}
