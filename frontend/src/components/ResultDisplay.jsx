import React from 'react';
import { CheckCircle, AlertTriangle, RefreshCw } from 'lucide-react';

const ResultDisplay = ({ result, reset }) => {
    const isFake = result.result === 'FAKE';
    const confidencePercent = (result.confidence * 100).toFixed(1);
    const color = isFake ? 'text-accent' : 'text-green-500';
    const bgGradient = isFake ? 'from-accent/20 to-transparent' : 'from-green-500/20 to-transparent';
    const borderColor = isFake ? 'border-accent/30' : 'border-green-500/30';

    return (
        <div className="py-20 px-4 min-h-[60vh] flex items-center justify-center">
            <div
                className={`max-w-2xl w-full glass-card p-8 rounded-2xl border ${borderColor} relative overflow-hidden`}
            >
                {/* Background Glow */}
                <div className={`absolute top-0 left-0 w-full h-1/2 bg-gradient-to-b ${bgGradient} blur-[60px] opacity-40 -z-10`}></div>

                <div className="text-center mb-8">
                    <div className="inline-block p-4 rounded-full bg-black/40 mb-4">
                        {isFake ? <AlertTriangle className="w-16 h-16 text-accent" /> : <CheckCircle className="w-16 h-16 text-green-500" />}
                    </div>
                    <h3 className="text-xl font-semibold text-gray-400 mb-1">VERDICT</h3>
                    <h2 className="text-5xl font-extrabold tracking-tight mb-2">
                        {isFake ? 'FAKE VIDEO' : 'REAL VIDEO'}
                    </h2>
                    <p className="text-gray-400">Analysis completed successfully</p>
                </div>

                <div className="grid md:grid-cols-2 gap-6 mb-8">
                    <div className="glass p-4 rounded-xl">
                        <p className="text-sm text-gray-400 mb-1">Confidence Score</p>
                        <div className="flex items-end space-x-2">
                            <span className={`text-3xl font-bold ${color}`}>{confidencePercent}%</span>
                        </div>
                        <div className="w-full bg-gray-700 h-2 rounded-full mt-3 overflow-hidden">
                            <div
                                className={`h-full ${isFake ? 'bg-accent' : 'bg-green-500'}`}
                                style={{ width: `${confidencePercent}%` }}
                            ></div>
                        </div>
                    </div>
                    <div className="glass p-4 rounded-xl">
                        <p className="text-sm text-gray-400 mb-1">Model Verdict</p>
                        <p className="text-lg text-white">
                            The model identified {result.details?.temporal_inconsistencies} temporal inconsistencies.
                        </p>
                    </div>
                </div>

                <div className="text-center">
                    <button
                        onClick={reset}
                        className="flex items-center justify-center space-x-2 mx-auto px-6 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all"
                    >
                        <RefreshCw className="w-4 h-4" />
                        <span>Analyze Another Video</span>
                    </button>
                </div>

            </div>
        </div>
    );
};

export default ResultDisplay;
