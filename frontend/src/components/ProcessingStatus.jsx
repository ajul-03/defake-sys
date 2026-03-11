import React, { useEffect, useState } from 'react';
import { Loader2 } from 'lucide-react';

const ProcessingStatus = () => {
    const [status, setStatus] = useState('Initializing...');

    useEffect(() => {
        const steps = [
            'Extracting frames...',
            'Detecting faces (MTCNN)...',
            'Analyzing facial artifacts...',
            'Checking temporal consistency (LSTM)...',
            'Finalizing prediction...'
        ];

        let i = 0;
        const interval = setInterval(() => {
            setStatus(steps[i]);
            i = (i + 1) % steps.length;
        }, 800);

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="py-20 px-4 min-h-[50vh] flex flex-col items-center justify-center">
            <div
                className="text-center"
            >
                <div className="relative w-24 h-24 mx-auto mb-8">
                    <div className="absolute inset-0 border-4 border-gray-800 rounded-full"></div>
                    <div className="absolute inset-0 border-4 border-primary rounded-full border-t-transparent animate-spin"></div>
                    <Loader2 className="absolute inset-0 m-auto w-10 h-10 text-primary animate-pulse" />
                </div>

                <h3 className="text-2xl font-bold text-white mb-2">Processing Video</h3>
                <p className="text-primary/80 font-mono">{status}</p>
            </div>
        </div>
    );
};

export default ProcessingStatus;
