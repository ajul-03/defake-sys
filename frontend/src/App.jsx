import React, { useState, useEffect } from 'react';
import axios from 'axios';
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';

// New Components
import TopNavbar from './components/TopNavbar';
import DataPanel from './components/DataPanel';
import ScannerVisual from './components/ScannerVisual';
import UploadDropzone from './components/UploadDropzone';

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('IDLE'); // IDLE, UPLOADING, PROCESSING, RESULT, ERROR
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Mock data for the realistic tech vibe
  const [cpuLoad, setCpuLoad] = useState(24);
  const [memUsage, setMemUsage] = useState(45);

  const [vramUsage, setVramUsage] = useState(72);
  const [gpuTemp, setGpuTemp] = useState(62);
  const [lastScanTime] = useState(new Date().toLocaleTimeString());

  // Simulate changing system metrics
  useEffect(() => {
    const interval = setInterval(() => {
        setCpuLoad(Math.floor(Math.random() * 20) + (status === 'PROCESSING' ? 70 : 20));
        setMemUsage(Math.floor(Math.random() * 15) + (status === 'PROCESSING' ? 80 : 40));
        setVramUsage(Math.floor(Math.random() * 20) + (status === 'PROCESSING' ? 70 : 10));
        setGpuTemp(Math.floor(Math.random() * 10) + (status === 'PROCESSING' ? 60 : 40));
    }, 2000);
    return () => clearInterval(interval);
  }, [status]);

  const leftPanelMetrics = [
      { label: 'CPU LOAD', value: `${cpuLoad}%`, progress: cpuLoad, alert: cpuLoad > 85 },
      { label: 'MEM USAGE', value: `${memUsage}%`, progress: memUsage, alert: memUsage > 90 },
      { label: 'NET UPLINK', value: '450 Mbps', progress: 75, alert: false },
      { label: 'NODE LATENCY', value: '12ms', progress: 10, alert: false },
      { label: 'SYS INTEGRITY', value: 'OPTIMAL', progress: 100, alert: false },
  ];

  // Right panel changes based on state
  const getRightPanelMetrics = () => {
      if (status === 'IDLE') {
          return [
              { label: 'TARGET', value: 'NONE', progress: 0, alert: false },
              { label: 'MODEL STATUS', value: 'STANDBY', progress: 100, alert: false },
              { label: 'LAST SCAN', value: lastScanTime, progress: 0, alert: false },
          ];
      }
      if (status === 'PROCESSING') {
          return [
              { label: 'TARGET', value: file?.name || 'UNKNOWN', progress: 100, alert: false },
              { label: 'MODEL STATUS', value: 'ACTIVE', progress: 100, alert: true },
              { label: 'VRAM USAGE', value: `${vramUsage}%`, progress: vramUsage, alert: false },
              { label: 'GPU TEMPS', value: `${gpuTemp}C`, progress: gpuTemp, alert: false },
          ];
      }
      if (status === 'RESULT' && result) {
          const isFake = result.result === 'FAKE';
          return [
              { label: 'THREAT LEVEL', value: isFake ? 'CRITICAL' : 'MINIMAL', progress: isFake ? 100 : 10, alert: isFake },
              { label: 'CONFIDENCE', value: `${(result.confidence * 100).toFixed(1)}%`, progress: result.confidence * 100, alert: isFake },
              { label: 'RAW SCORE', value: result.raw_score?.toFixed(4) || 'N/A', progress: 50, alert: false },
          ];
      }
      return [];
  };

  const handleFileSelect = async (selectedFile) => {
    setFile(selectedFile);
    setStatus('PROCESSING');
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await axios.post('http://127.0.0.1:5000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      // Artificial delay for dramatic effect
      setTimeout(() => {
          setResult(response.data);
          setStatus('RESULT');
      }, 1500);

    } catch (err) {
      console.error(err);
      const errorMessage = err.response?.data?.error || err.message || 'Unknown error';
      setError(`Failed: ${errorMessage}`);
      setStatus('ERROR');
    }
  };

  const reset = () => {
    setFile(null);
    setResult(null);
    setError(null);
    setStatus('IDLE');
  };

  return (
    <div className="min-h-screen bg-[#050b14] text-[#e2e8f0] font-mono selection:bg-[#00ffff]/30 flex flex-col relative overflow-hidden">
      <TopNavbar />

      {/* Main Grid Layout */}
      <main className="flex-1 mt-16 p-4 grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-4rem)]">
        
        {/* Left Side: System Data */}
        <div className="hidden lg:block lg:col-span-1 h-full">
            <DataPanel side="left" title="SYSTEM METRICS" metrics={leftPanelMetrics} />
        </div>

        {/* Center: Main Scanner & UI */}
        <div className="col-span-1 lg:col-span-2 flex flex-col h-full cyber-panel rounded p-6 relative">
            <div className="flex-1 flex flex-col items-center justify-center relative z-10 space-y-8 h-full">
                
                {/* Visual Scanner */}
                <ScannerVisual status={status} result={result} />

                {/* Interaction Area */}
                <div className="w-full max-w-md mt-auto">
                    <AnimatePresence mode="wait">
                        {status === 'IDLE' && (
                            <motion.div
                                key="idle"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                            >
                                <UploadDropzone onFileSelect={handleFileSelect} />
                            </motion.div>
                        )}

                        {status === 'PROCESSING' && (
                             <motion.div
                                key="processing"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                className="text-center space-y-4"
                             >
                                 <div className="h-1 w-full bg-[#0f172a] rounded overflow-hidden">
                                     <motion.div
                                         initial={{ x: '-100%' }}
                                         animate={{ x: '100%' }}
                                         transition={{ repeat: Infinity, duration: 2, ease: "linear" }}
                                         className="h-full w-1/2 bg-[#00ffff] shadow-[0_0_10px_#00ffff]"
                                     />
                                 </div>
                                 <p className="text-sm text-[#00ffff] animate-pulse glow-text tracking-widest">EXECUTING NEURAL ANALYSIS...</p>
                                 {file && <p className="text-xs text-[#64748b]">TARGET: {file.name}</p>}
                             </motion.div>
                        )}

                        {status === 'RESULT' && result && (
                            <motion.div
                                key="result"
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="w-full"
                            >
                                 <button
                                     onClick={reset}
                                     className="w-full font-mono font-bold tracking-widest py-3 cyber-panel hover:bg-[#00ffff]/10 hover:border-[#00ffff] text-[#00ffff] transition-all uppercase"
                                 >
                                     [ NEW SCAN SEQUENCE ]
                                 </button>
                            </motion.div>
                        )}
                        
                        {status === 'ERROR' && (
                            <div className="text-center p-4 border border-[#ff3333] bg-[#ff3333]/10">
                                <p className="text-[#ff3333] font-bold">SYSTEM ERROR</p>
                                <p className="text-sm text-[#ff3333]/80">{error}</p>
                                <button onClick={reset} className="mt-4 px-4 py-2 border border-[#ff3333] hover:bg-[#ff3333]/20 text-[#ff3333] text-sm tracking-widest">
                                    [ RESET SYSTEM ]
                                </button>
                            </div>
                        )}
                    </AnimatePresence>
                </div>
            </div>

            {/* Background Grid Lines for center panel */}
            <div className="absolute inset-0 z-0 bg-transparent flex flex-wrap justify-between items-center pointer-events-none opacity-20">
                <div className="w-full h-px bg-[#00ffff]"></div>
                <div className="h-full w-px bg-[#00ffff] ml-auto"></div>
            </div>
        </div>

        {/* Right Side: Analysis Data */}
        <div className="hidden lg:block lg:col-span-1 h-full">
            <DataPanel side="right" title="ANALYSIS FEED" metrics={getRightPanelMetrics()} />
        </div>
      </main>

    </div>
  );
}

export default App;
