import React from 'react';
import { ShieldCheck, Crosshair, Activity, Cpu } from 'lucide-react';

const TopNavbar = () => {
    return (
        <nav className="w-full cyber-panel fixed top-0 z-50 h-16 flex justify-between items-center px-6 border-b border-[#00ffff]/20">
            {/* Logo */}
            <div className="flex items-center space-x-3">
                <ShieldCheck className="w-8 h-8 text-[#00ffff] animate-pulse" />
                <span className="text-xl font-bold tracking-[0.2em] text-[#00ffff] glow-text">DEFAKE.SYS</span>
                <span className="text-xs text-[#64748b] ml-4 hidden md:block border-l border-[#64748b] pl-4">V_2.0.4.ONLINE</span>
            </div>

            {/* Central Status Indicators */}
            <div className="hidden lg:flex items-center space-x-8">
               <div className="flex items-center space-x-2 text-xs font-mono">
                   <Activity className="w-4 h-4 text-green-400" />
                   <span className="text-green-400">SERVER: CONNECTED</span>
               </div>
               <div className="flex items-center space-x-2 text-xs font-mono">
                   <Cpu className="w-4 h-4 text-[#00ffff]" />
                   <span className="text-[#e2e8f0]">NODE: ACTIVE</span>
               </div>
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center space-x-4">
               <button className="flex items-center space-x-2 border border-[#0055ff] hover:bg-[#0055ff]/20 text-[#00ffff] px-4 py-1.5 rounded transition-all text-sm font-mono uppercase">
                   <Crosshair className="w-4 h-4" />
                   <span>Initialize Scan</span>
               </button>
            </div>
        </nav>
    );
};

export default TopNavbar;
