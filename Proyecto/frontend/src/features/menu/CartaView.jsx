import React, { useState, useEffect } from 'react';
import DishCard from './components/DishCard';
import ShoppingCart from '../cart/components/ShoppingCart';
import { apiClient } from '../../core/api';

const CartaView = ({ cartItems, setCartItems }) => {
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleAddToCart = (dish) => {
    setCartItems(prev => {
      const existing = prev.find(i => i.id_plato === dish.id_plato);
      if (existing) {
        return prev.map(i => i.id_plato === dish.id_plato ? { ...i, cantidad: i.cantidad + 1 } : i);
      }
      return [...prev, { ...dish, cantidad: 1 }];
    });
  };

  useEffect(() => {
    const fetchDishes = async () => {
      try {
        const res = await apiClient.get('/dishes');
        // Filtramos para asegurar que no se cuele data corrompida y mostramos solo los destinados a carta
        const filteredDishes = res.data.filter(d => d.visibilidad === 'CARTA' || d.visibilidad === 'AMBOS');
        setDishes(filteredDishes);
      } catch (err) {
        console.error("Error cargando la carta:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDishes();
  }, []);

  return (
    <div className="flex flex-col lg:flex-row gap-12">
        {/* Zona de Catálogo (Grid Dinámico Disperso) */}
        <div className="flex-1 animate-fade-in">
          <h2 className="text-4xl font-display font-black text-brand-dark mb-2">Nuestra Carta</h2>
          <p className="text-slate-500 mb-8 border-b border-slate-200 pb-4">Elige tus platos favoritos de forma individual.</p>
          
          {loading ? (
             <div className="text-center py-20 text-slate-500 font-bold animate-pulse">Cocinando la Carta...</div>
          ) : dishes.length === 0 ? (
             <div className="text-center py-20 bg-slate-50 border border-dashed border-slate-200 rounded-2xl">
                <span className="text-slate-400">Pronto llegarán nuevos platos...</span>
             </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {dishes.map(dish => (
                <DishCard key={dish.id_plato} dish={dish} onAddToCart={handleAddToCart} />
              ))}
            </div>
          )}
        </div>

        {/* Zona Lateral del checkout */}
        <aside className="w-full lg:w-[400px]">
          <div className="sticky top-28">
            <ShoppingCart items={cartItems} setItems={setCartItems} />
          </div>
        </aside>
    </div>
  );
};

export default CartaView;
