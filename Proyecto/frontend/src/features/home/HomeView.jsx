import React from 'react';
import { Link } from 'react-router-dom';

const HomeView = () => {
  return (
    <div className="animate-fade-in space-y-16">
      
      {/* Hero Section */}
      <div className="relative rounded-3xl overflow-hidden h-[500px] flex items-center shadow-2xl bg-brand-dark">
        <div className="absolute inset-0 bg-gradient-to-r from-brand-dark via-brand-dark/90 to-transparent z-10 w-2/3"></div>
        {/* Usamos un degradado cálido para simular la textura picante/nepalí */}
        <div className="absolute inset-0 bg-gradient-to-tr from-amber-600/30 to-brand-primary/20 mix-blend-color-burn"></div>
        <img 
          src="https://images.unsplash.com/photo-1585937421612-70a008356fbe?q=80&w=2000" 
          className="absolute right-0 top-0 h-full w-1/2 object-cover opacity-70"
          alt="Himalayan food"
        />
        
        <div className="relative z-20 px-12 md:px-24">
          <span className="text-brand-accent font-bold tracking-widest uppercase text-sm mb-4 block">Especialidades del Himalaya</span>
          <h1 className="text-5xl md:text-7xl font-display font-black text-white mb-6 leading-tight">
            Descubre el<br />Auténtico Sabor
          </h1>
          <p className="text-gray-300 max-w-lg text-lg mb-8">
            Disfruta de nuestros currys cremosos, panes naan horneados al momento y platos tradicionales directamente en tu casa.
          </p>
          <div className="flex gap-4">
            <Link to="/carta" className="bg-brand-primary hover:bg-rose-700 text-white px-8 py-4 rounded-full font-bold shadow-[0_0_15px_rgba(225,29,72,0.4)] transition-all transform hover:-translate-y-1">
              Ver Carta Completa
            </Link>
            <Link to="/menu-diario" className="bg-white hover:bg-gray-100 text-brand-dark px-8 py-4 rounded-full font-bold shadow-xl transition-all">
              Menú del Día (15€)
            </Link>
          </div>
        </div>
      </div>

      {/* Novedades / Ofertas */}
      <div>
        <div className="flex items-center justify-between mb-8 border-b-2 border-brand-accent pb-2">
          <h2 className="text-3xl font-display font-bold text-slate-800">Novedades & Ofertas</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gradient-to-br from-amber-100 to-orange-50 border border-amber-200 p-8 rounded-2xl relative overflow-hidden group hover:shadow-xl transition-all cursor-pointer">
              <div className="absolute -right-10 -top-10 w-32 h-32 bg-amber-400 rounded-full blur-3xl opacity-50 group-hover:opacity-80 transition-opacity"></div>
              <h3 className="text-2xl font-bold text-slate-800 mb-2">Descuento de Auténticos</h3>
              <p className="text-slate-600 mb-4">Si te registras, por cada 100€ gastados acumularás automáticamente 5€ limpios de descuento en tu cuenta.</p>
              <span className="text-amber-600 font-bold">Crear cuenta →</span>
            </div>
            
            <div className="bg-slate-800 text-white p-8 rounded-2xl relative overflow-hidden group hover:shadow-xl transition-all cursor-pointer">
              <div className="absolute -right-10 -top-10 w-32 h-32 bg-brand-primary rounded-full blur-3xl opacity-30 group-hover:opacity-60 transition-opacity"></div>
              <h3 className="text-2xl font-bold mb-2">Nuevo Plato del Chef</h3>
              <p className="text-slate-300 mb-4">Prueba nuestro Cordero Rogan Josh extra picante. Solo por tiempo limitado en la sección Tandoori.</p>
              <Link to="/carta" className="text-brand-accent font-bold">Ver novedades →</Link>
            </div>
        </div>
      </div>

    </div>
  );
};

export default HomeView;
