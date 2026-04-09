import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';

import HomeView from './features/home/HomeView';
import CartaView from './features/menu/CartaView';
import DailyMenuView from './features/menu/DailyMenuView';
import ChefLogin from './features/auth/ChefLogin';

const Navbar = () => {
    const location = useLocation();
    const isChef = location.pathname.startsWith('/chef-admin');
    
    // Si estamos en la página del chef de administración total, no mostramos la barra comercial (O mostramos advertencia)
    if (isChef) return null;

    return (
      <header className="bg-brand-dark text-white shadow-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-20 flex items-center justify-between">
          <Link to="/" className="text-2xl font-display font-black tracking-tight flex items-center gap-2">
            🏔️ <span className="text-brand-accent">Sabor del</span> Himalaya
          </Link>
          <nav className="hidden md:flex gap-6 font-semibold text-sm">
            <Link to="/carta" className="hover:text-brand-accent text-white transition-colors">Carta Tradicional</Link>
            <Link to="/menu-diario" className="text-amber-400 hover:text-white transition-colors font-bold flex items-center gap-2">
               <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span> Menú Diario
            </Link>
          </nav>
        </div>
      </header>
    )
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 py-12 w-full flex-grow">
          <Routes>
            <Route path="/" element={<HomeView />} />
            <Route path="/carta" element={<CartaView />} />
            <Route path="/menu-diario" element={<DailyMenuView />} />
            
            {/* Oculta del menú, accesible solo por URL */}
            <Route path="/chef-admin/*" element={<ChefLogin />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
