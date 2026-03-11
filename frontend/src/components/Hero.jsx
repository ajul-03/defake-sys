import React from 'react';

const Hero = () => {
    return (
        <section className="relative h-screen flex flex-col justify-center items-center text-center px-4 overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 blur-[120px] rounded-full animate-pulse-slow"></div>
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/20 blur-[120px] rounded-full animate-pulse-slow" style={{ animationDelay: '1.5s' }}></div>
            </div>

            <div
                className="max-w-4xl"
            >
                <span className="inline-block px-4 py-1.5 rounded-full border border-primary/30 bg-primary/10 text-primary text-sm font-semibold mb-6">
                    Advanced Deepfake Detection
                </span>
                <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                    Unmask the <br /> <span className="text-primary">Artificial Reality</span>
                </h1>
                <p className="text-lg md:text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
                    Protect integrity with our state-of-the-art AI detection system.
                    Analyze videos in real-time to identify manipulated content with high precision.
                </p>

                <div className="flex justify-center space-x-4">
                    <a href="#demo" className="px-8 py-3 bg-primary hover:bg-primary/90 text-black font-bold rounded-lg transition-all shadow-lg shadow-primary/25">
                        Try Demo
                    </a>
                    <button className="px-8 py-3 border border-gray-600 hover:border-white hover:bg-white/5 text-white font-medium rounded-lg transition-all">
                        Learn More
                    </button>
                </div>
            </div>
        </section>
    );
};

export default Hero;
