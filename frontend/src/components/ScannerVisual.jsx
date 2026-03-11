import React from 'react';
import { ScanFace } from 'lucide-react';

const ScannerVisual = ({ status, result }) => {
    // Determine color based on state
    let scanColor = "border-[#00ffff]";
    let glowColor = "rgba(0, 255, 255, 0.4)";
    let isScanning = status === 'PROCESSING';
    
    if (status === 'RESULT' && result) {
        if (result.result === 'FAKE') {
            scanColor = "border-[#ff3333]";
            glowColor = "rgba(255, 51, 51, 0.6)";
        } else {
            scanColor = "border-green-500";
            glowColor = "rgba(34, 197, 94, 0.6)";
        }
    }

    return (
        <div className="relative w-full max-w-lg aspect-[3/4] mx-auto flex items-center justify-center">
            {/* Outer Target Box */}
            <div className={`absolute inset-0 border-2 ${scanColor} opacity-50 transition-colors duration-500`}>
                {/* Corner Accents */}
                <div className={`absolute top-0 left-0 w-16 h-16 border-t-4 border-l-4 ${scanColor}`}></div>
                <div className={`absolute top-0 right-0 w-16 h-16 border-t-4 border-r-4 ${scanColor}`}></div>
                <div className={`absolute bottom-0 left-0 w-16 h-16 border-b-4 border-l-4 ${scanColor}`}></div>
                <div className={`absolute bottom-0 right-0 w-16 h-16 border-b-4 border-r-4 ${scanColor}`}></div>
            </div>

            {/* Central Hologram/Icon Area */}
            <div className="relative z-10 p-12 bg-black/40 rounded-full backdrop-blur-sm border border-[#00ffff]/20">
                 <ScanFace className={`w-32 h-32 ${status === 'RESULT' && result?.result === 'FAKE' ? 'text-[#ff3333]' : 'text-[#00ffff]'}`} strokeWidth={1} />
            </div>

            {/* Scanning Laser Animation */}
            {isScanning && (
                <div className="absolute inset-0 overflow-hidden pointer-events-none z-20">
                    <div className="w-full h-1 bg-[#00ffff] animate-scan shadow-[0_0_15px_#00ffff]" />
                    {/* Glowing scanning wash */}
                    <div className="w-full h-32 bg-gradient-to-b from-transparent via-[#00ffff]/10 to-[#00ffff]/30 animate-scan -mt-32 backdrop-blur-[2px]" />
                </div>
            )}

            {/* Status Text Overlay */}
            <div className="absolute bottom-4 text-center w-full font-mono text-sm tracking-widest uppercase">
                {status === 'IDLE' && <span className="text-[#00ffff] glow-text">AWAITING TARGET SIGNAL...</span>}
                {status === 'PROCESSING' && <span className="text-[#00ffff] animate-pulse glow-text">ANALYZING BIOMETRICS...</span>}
                {status === 'RESULT' && (
                    <span className={result?.result === 'FAKE' ? 'text-[#ff3333] glow-text-red font-bold' : 'text-green-500 font-bold'}>
                        VERDICT: {result?.result} MATCH
                    </span>
                )}
            </div>
            
             {/* Background Pulse Rings */}
             {isScanning && (
                 <>
                    <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 border border-[#00ffff]/40 rounded-full animate-pulse-ring`}></div>
                    <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 border border-[#00ffff]/20 rounded-full animate-pulse-ring`} style={{animationDelay: '0.5s'}}></div>
                 </>
             )}
             
             {/* Ambient Glow */}
             <div className="absolute inset-0 bg-gradient-to-t from-transparent via-transparent to-transparent z-0" style={{boxShadow: `0 0 100px ${glowColor}`}}></div>
        </div>
    );
};

export default ScannerVisual;
