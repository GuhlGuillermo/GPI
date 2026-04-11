import React, { useState } from 'react';
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
  const [cartItems, setCartItems] = useState([]);

  const addToCart = (product) => {
    setCartItems(prev => {
      const existing = prev.find(item => item.dish_id === product.dish_id);
      if (existing) {
        return prev.map(item => 
          item.dish_id === product.dish_id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prev, { ...product, id: Date.now().toString(), quantity: 1 }];
    });
  };

  return (
    <Router>
      <div className="min-h-screen bg-slate-50 flex flex-col">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 py-12 w-full flex-grow">
          <Routes>
            <Route path="/" element={<HomeView />} />
            {/* [MODIFICADO] Pasamos el carrito y la función de añadir */}
            <Route path="/carta" element={
              <CartaView 
                cartItems={cartItems} 
                setCartItems={setCartItems} 
                onAdd={addToCart} 
              />
            } />
            {/* [MODIFICADO] Pasamos la función al menú diario */}
            <Route path="/menu-diario" element={
              <DailyMenuView onAdd={addToCart} />
            } />
            <Route path="/chef-admin/*" element={<ChefLogin />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
