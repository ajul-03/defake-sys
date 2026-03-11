import React from 'react';
import { Activity, ShieldAlert, Fingerprint, Zap } from 'lucide-react';
import { cn } from '../lib/utils';
// import { motion } from 'framer-motion';

const DataPanel = ({ side, title, metrics }) => {
    const isLeft = side === 'left';
    
    return (
        <div className={cn(
            "h-full cyber-panel p-4 flex flex-col hidden lg:flex",
            isLeft ? "border-r border-[#00ffff]/20" : "border-l border-[#00ffff]/20"
        )}>
            {/* Panel Header */}
            <div className="flex items-center space-x-2 border-b border-[#00ffff]/30 pb-3 mb-4">
                {isLeft ? <Activity className="w-5 h-5 text-[#00ffff]" /> : <ShieldAlert className="w-5 h-5 text-[#00ffff]" />}
                <h3 className="text-sm font-bold tracking-widest text-[#00ffff] uppercase glow-text">{title}</h3>
            </div>

            {/* Content Area */}
            <div className="flex-1 overflow-y-auto space-y-6 pr-2">
                {metrics.map((metric, idx) => (
                    <div key={idx} className="bg-black/40 border border-[#00ffff]/10 p-3 rounded">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-xs text-[#64748b] font-mono uppercase">{metric.label}</span>
                            <span className={cn("text-xs font-bold font-mono", metric.alert ? "text-[#ff3333] glow-text-red" : "text-[#e2e8f0]")}>
                                {metric.value}
                            </span>
                        </div>
                        
                        {/* Fake Progress/Visual Bar */}
                        <div className="w-full h-1.5 bg-[#0f172a] rounded overflow-hidden">
                            <div 
                                className={cn("h-full transition-all duration-1000 ease-out", metric.alert ? "bg-[#ff3333]" : "bg-[#00ffff]")}
                                style={{ width: `${metric.progress}%` }}
                            />
                        </div>
                    </div>
                ))}

                {/* Decorative Tech Element */}
                <div className="mt-auto pt-6 border-t border-[#00ffff]/10 relative">
                    <div className="absolute top-0 right-0 w-8 h-8 border-t border-r border-[#00ffff]/30" />
                    <div className="flex items-center justify-between text-[#00ffff]/50 text-xs font-mono">
                        <span className="flex items-center gap-1"><Fingerprint className="w-3 h-3"/> ID: A7X-99</span>
                        <span className="flex items-center gap-1"><Zap className="w-3 h-3"/> PWR: OPT</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DataPanel;
