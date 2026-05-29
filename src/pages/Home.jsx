import { useState } from "react";
import { Link } from "react-router-dom";
import items from "../data/items";
import RatingWidget from "../components/RatingWidget"; 
import PurchaseButton from "../components/PurchaseButton"; 

function Home({ searchQuery = "" }) {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [maxPrice, setMaxPrice] = useState(100);

  const categories = ["All", ...new Set(items.map(item => item.category))];
  const highestPrice = Math.max(...items.map(item => item.price), 100);

  const filteredItems = items.filter((item) => {
    const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === "All" || item.category === selectedCategory;
    const matchesPrice = item.price <= maxPrice;
    
    return matchesSearch && matchesCategory && matchesPrice;
  });

  return (
    <main className="page home-page">
      <section className="home-hero">
        <div>
          <p className="hero-eyebrow">Curated marketplace</p>
          <h1 className="hero-title">
            Discover premium products that feel made for you.
          </h1>
          <p className="hero-copy">
            Shop everyday favorites across home, tech, fitness, and lifestyle.
            Every item is selected for quality, value, and real usefulness.
          </p>
        </div>
      </section>

      <section style={{ display: 'flex', gap: '20px', alignItems: 'center', flexWrap: 'wrap', marginBottom: '1rem', padding: '1rem', background: 'var(--bg-card)', borderRadius: '12px', border: '1px solid var(--border)' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <label style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Category Filter</label>
          <select 
            value={selectedCategory} 
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={{ padding: '6px', borderRadius: '4px', background: 'var(--bg-input)', color: 'var(--text)', border: '1px solid var(--border)' }}
          >
            {categories.map(cat => <option key={cat} value={cat}>{cat}</option>)}
          </select>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px', flexGrow: 1, maxWidth: '300px' }}>
          <label style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
            Max Price: ₹{maxPrice}
          </label>
          <input 
            type="range" 
            min="0" 
            max={highestPrice} 
            value={maxPrice} 
            onChange={(e) => setMaxPrice(Number(e.target.value))}
            style={{ accentColor: 'var(--text)' }}
          />
        </div>
      </section>

      <section className="item-grid">
        {filteredItems.length > 0 ? (
          filteredItems.map((item) => (
            <div key={item.id} className="item-card">
              <div className="item-card-image">
                <img src={item.image} alt={item.name} />
                <span className="item-card-label">{item.category}</span>
              </div>
              
              <div className="item-card-body">
                <Link to={`/item/${item.id}`} className="item-name">{item.name}</Link>
                <p className="item-desc line-clamp-2">{item.description}</p>
                
                <div style={{ marginTop: 'auto' }}>
                  <RatingWidget />
                </div>
              </div>

              <div className="item-card-footer">
                <span className="item-price">₹{item.price.toFixed(2)}</span>
                <PurchaseButton item={item} />
              </div>
            </div>
          ))
        ) : (
          <p className="empty-state" style={{ gridColumn: '1 / -1' }}>
            No products match your current filters and search.
          </p>
        )}
      </section>
    </main>
  );
}

export default Home;