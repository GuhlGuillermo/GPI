import React from 'react';

const DishCard = ({ 
    dish = { dish_id: 'D1', name: 'Momo de Pollo', description: 'Empanadillas al vapor rellenas de carne marinada con especias del Himalaya.', snapshot_price: 6.50, category: 'Entrantes' },
    onAdd
}) => {
  return (
    <div className="bg-white rounded-2xl shadow-xl overflow-hidden hover:-translate-y-1 transition-transform duration-300 border border-slate-100 flex flex-col h-full group">
      {/* Etiqueta de Categoría Flotante */}
      <div className="relative h-48 bg-slate-800 overflow-hidden">
        {/* Placeholder para la imagen real, usamos un gradiente bonito y patrón */}
        <div className="absolute inset-0 bg-gradient-to-br from-amber-600/80 to-slate-900/90 mix-blend-multiply group-hover:scale-105 transition-transform duration-500"></div>
        <span className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm text-slate-800 text-xs font-bold px-3 py-1 rounded-full shadow-sm">
          {dish.category}
        </span>
        <h3 className="absolute bottom-4 left-4 text-white text-2xl font-bold tracking-tight">
          {dish.name}
        </h3>
      </div>
      
      {/* Contenido / Descripción */}
      <div className="p-5 flex-grow flex flex-col">
        <p className="text-slate-500 text-sm flex-grow line-clamp-3">
          {dish.description}
        </p>
        
        {/* Botonera y Precio inferior */}
        <div className="mt-6 flex items-center justify-between">
          <span className="text-2xl font-extrabold text-slate-800">
            {dish.snapshot_price ? dish.snapshot_price.toFixed(2) : "0.00"}€
          </span>
          <button 
            onClick={() => onAdd && onAdd(dish)}
            className="bg-amber-500 hover:bg-amber-600 active:bg-amber-700 text-white font-semibold py-2 px-5 rounded-xl shadow-lg shadow-amber-500/30 transition-all focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2"
          >
            + Añadir
          </button>
        </div>
      </div>
    </div>
  );
};

export default DishCard;
