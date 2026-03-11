import React from 'react';
import { ShieldCheck, Github } from 'lucide-react';

const Navbar = () => {
    return (
        <nav className="w-full glass fixed top-0 z-50 px-6 py-4 flex justify-between items-center text-white">
            <div className="flex items-center space-x-2">
                <ShieldCheck className="w-8 h-8 text-primary" />
                <span className="text-xl font-bold tracking-wider">DEFAKE<span className="text-primary">.AI</span></span>
            </div>
            <div className="hidden md:flex space-x-8 text-sm font-medium text-gray-300">
                <a href="#" className="hover:text-primary transition-colors">Home</a>
                <a href="#demo" className="hover:text-primary transition-colors">Detect</a>
                <a href="#about" className="hover:text-primary transition-colors">About</a>
                <a href="#" className="hover:text-primary transition-colors">API</a>
            </div>
            <div>
                <a href="#" className="flex items-center space-x-2 bg-white/10 hover:bg-white/20 px-4 py-2 rounded-full transition-all">
                    <Github className="w-4 h-4" />
                    <span className="text-sm">Star on GitHub</span>
                </a>
            </div>
        </nav>
    );
};

export default Navbar;
