import React, { useState, useEffect } from 'react';
import { Search, Bell, Flag, Settings, Home, Heart, Compass, TrendingUp, PlayCircle, Filter, ChevronRight, Plus, X, Music2, Share2, Eye, Camera, Sparkles, Palette, Users, Tv } from 'lucide-react';

interface Brand {
  id: string;
  name: string;
  videoUrl: string;
  thumbnail: string;
  category: string;
  followers: number;
  location: string;
  description?: string;
  dropDate?: string;
}

interface Designer {
  id: string;
  name: string;
  image: string;
  role: string;
  brand: string;
  followers: number;
  featured: boolean;
}

interface RunwayShow {
  id: string;
  brand: string;
  season: string;
  location: string;
  thumbnail: string;
  videoUrl: string;
  views: number;
  duration: string;
}

const designers: Designer[] = [
  {
    id: '1',
    name: 'Yohji Yamamoto',
    image: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=300&q=80',
    role: 'Creative Director',
    brand: 'Y-3',
    followers: 1500000,
    featured: true
  },
  {
    id: '2',
    name: 'Rei Kawakubo',
    image: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80',
    role: 'Founder',
    brand: 'Comme des Garçons',
    followers: 2000000,
    featured: true
  }
];

const runwayShows: RunwayShow[] = [
  {
    id: '1',
    brand: 'ACRONYM',
    season: 'FW24',
    location: 'Tokyo',
    thumbnail: 'https://images.unsplash.com/photo-1550614000-4895a10e1bfd?auto=format&fit=crop&w=800&q=80',
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-fashion-model-walking-on-city-street-34671-large.mp4',
    views: 1200000,
    duration: '12:34'
  },
  {
    id: '2',
    brand: 'NEURAL',
    season: 'SS24',
    location: 'Paris',
    thumbnail: 'https://images.unsplash.com/photo-1469334031218-e382a71b716b?auto=format&fit=crop&w=800&q=80',
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-young-woman-modeling-for-a-photo-shoot-34486-large.mp4',
    views: 890000,
    duration: '15:20'
  }
];

const trendingBrands: Brand[] = [
  {
    id: '1',
    name: 'ACRONYM',
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-fashion-model-walking-on-city-street-34671-large.mp4',
    thumbnail: 'https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?auto=format&fit=crop&w=600&q=80',
    category: 'TECH WEAR',
    followers: 1200000,
    location: 'Berlin',
    description: 'The future of technical apparel',
    dropDate: '2024-03-15'
  },
  {
    id: '2',
    name: 'NEURAL',
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-young-woman-modeling-for-a-photo-shoot-34486-large.mp4',
    thumbnail: 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=600&q=80',
    category: 'AI FASHION',
    followers: 2500000,
    location: 'Tokyo',
    description: 'AI-generated designs, human-crafted quality',
    dropDate: '2024-03-18'
  },
  {
    id: '3',
    name: 'VOID',
    videoUrl: 'https://assets.mixkit.co/videos/preview/mixkit-woman-modeling-in-the-street-34480-large.mp4',
    thumbnail: 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=600&q=80',
    category: 'AVANT-GARDE',
    followers: 800000,
    location: 'Paris',
    description: 'Pushing boundaries since 2020',
    dropDate: '2024-03-20'
  }
];

function App() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [cursorVariant, setCursorVariant] = useState('default');
  const [selectedBrand, setSelectedBrand] = useState<Brand | null>(null);
  const [showReel, setShowReel] = useState(false);
  const [activeSection, setActiveSection] = useState('home');

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const navItems = [
    { id: 'home', icon: Home, label: 'HOME' },
    { id: 'explore', icon: Compass, label: 'EXPLORE' },
    { id: 'designers', icon: Users, label: 'DESIGNERS' },
    { id: 'runway', icon: Camera, label: 'RUNWAY' },
    { id: 'saved', icon: Heart, label: 'SAVED' }
  ];

  return (
    <div className="min-h-screen text-white overflow-hidden">
      {/* Custom Cursor */}
      <div
        className="custom-cursor fixed w-6 h-6 bg-white rounded-full pointer-events-none z-50 transition-transform duration-100 ease-out"
        style={{
          transform: `translate(${mousePosition.x - 12}px, ${mousePosition.y - 12}px)`,
          mixBlendMode: 'difference'
        }}
      />

      {/* Enhanced Navigation */}
      <nav className="fixed left-0 top-0 h-full w-24 bg-gradient-to-b from-white/5 to-transparent backdrop-blur-lg z-40 flex flex-col items-center py-8 border-r border-white/5">
        <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl mb-12 flex items-center justify-center">
          <span className="text-xl font-bold">UN</span>
        </div>
        <div className="flex-1 flex flex-col gap-8">
          {navItems.map(({ id, icon: Icon, label }) => (
            <button
              key={id}
              className={`group relative p-3 transition-all duration-300 ${
                activeSection === id ? 'bg-white/10 rounded-xl' : ''
              }`}
              onClick={() => setActiveSection(id)}
            >
              <Icon className={`w-6 h-6 transition-colors duration-300 ${
                activeSection === id ? 'text-white' : 'text-white/50'
              }`} />
              <div className="absolute left-full ml-4 px-3 py-1 bg-white/10 rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 whitespace-nowrap backdrop-blur-lg">
                {label}
              </div>
              {activeSection === id && (
                <div className="absolute right-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-purple-500 to-pink-500 rounded-l-full" />
              )}
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="ml-24 min-h-screen pt-8 px-12">
        {/* Header */}
        <header className="flex justify-between items-center mb-16 sticky top-0 z-30 py-4 bg-black/50 backdrop-blur-lg">
          <div className="flex items-center gap-12">
            <h1 className="text-4xl font-bold tracking-tighter">
              UN<span className="text-stroke">ARCHIVED</span>
            </h1>
            <div className="flex items-center gap-8 text-sm">
              <button className="px-4 py-2 rounded-lg hover:bg-white/5 transition-colors">TRENDING</button>
              <button className="px-4 py-2 rounded-lg hover:bg-white/5 transition-colors">NEW DROPS</button>
              <button className="px-4 py-2 rounded-lg hover:bg-white/5 transition-colors">LIVE</button>
            </div>
          </div>
          <div className="flex items-center gap-8">
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
              <input
                type="text"
                placeholder="Search collections..."
                className="w-64 bg-white/5 border border-white/10 rounded-full py-3 pl-12 pr-4 focus:outline-none focus:border-white/20 transition-colors"
              />
            </div>
            <div className="flex items-center gap-6">
              <Bell className="w-6 h-6 text-white/50 hover:text-white cursor-pointer transition-colors" />
              <div className="relative">
                <img
                  src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=32&h=32&q=80"
                  alt="Profile"
                  className="w-10 h-10 rounded-xl ring-2 ring-white/20 cursor-pointer"
                />
                <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-black" />
              </div>
            </div>
          </div>
        </header>

        {/* Featured Designers */}
        <section className="mb-20">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold">Featured Designers</h2>
            <button className="flex items-center gap-2 text-white/50 hover:text-white transition-colors">
              View all <ChevronRight className="w-4 h-4" />
            </button>
          </div>
          <div className="grid grid-cols-2 gap-8">
            {designers.map(designer => (
              <div key={designer.id} className="group relative h-80 rounded-3xl overflow-hidden">
                <img
                  src={designer.image}
                  alt={designer.name}
                  className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />
                <div className="absolute inset-0 p-8 flex flex-col justify-end">
                  <div className="space-y-2">
                    <div className="flex items-center gap-3">
                      <span className="px-3 py-1 rounded-full bg-white/10 backdrop-blur-sm text-xs font-medium">
                        {designer.role}
                      </span>
                      <span className="text-white/70 text-sm">{designer.brand}</span>
                    </div>
                    <h3 className="text-3xl font-bold">{designer.name}</h3>
                    <p className="text-white/70">{(designer.followers / 1000000).toFixed(1)}M Followers</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Runway Shows */}
        <section className="mb-20">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold">Latest Runway Shows</h2>
            <button className="flex items-center gap-2 text-white/50 hover:text-white transition-colors">
              View all <ChevronRight className="w-4 h-4" />
            </button>
          </div>
          <div className="grid grid-cols-2 gap-8">
            {runwayShows.map(show => (
              <div key={show.id} className="group relative aspect-video rounded-3xl overflow-hidden">
                <video
                  loop
                  muted
                  playsInline
                  className="absolute inset-0 w-full h-full object-cover opacity-0 group-hover:opacity-100 transition-opacity duration-700"
                  onMouseEnter={(e) => (e.currentTarget as HTMLVideoElement).play()}
                  onMouseLeave={(e) => (e.currentTarget as HTMLVideoElement).pause()}
                >
                  <source src={show.videoUrl} type="video/mp4" />
                </video>
                <img
                  src={show.thumbnail}
                  alt={show.brand}
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent" />
                <div className="absolute inset-0 p-6 flex flex-col justify-between">
                  <div className="flex justify-between items-start">
                    <span className="px-3 py-1 rounded-full bg-white/10 backdrop-blur-sm text-xs font-medium">
                      {show.season}
                    </span>
                    <div className="glass-card px-3 py-1 rounded-full flex items-center gap-2">
                      <Eye className="w-4 h-4" />
                      <span className="text-sm">{(show.views / 1000).toFixed(0)}K</span>
                    </div>
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold mb-2">{show.brand}</h3>
                    <div className="flex items-center justify-between">
                      <span className="text-white/70">{show.location}</span>
                      <span className="text-white/70">{show.duration}</span>
                    </div>
                  </div>
                </div>
                <button className="absolute inset-0 w-full h-full flex items-center justify-center bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <PlayCircle className="w-16 h-16" />
                </button>
              </div>
            ))}
          </div>
        </section>

        {/* Featured Brands */}
        <section className="mb-20">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold">Featured Brands</h2>
            <button className="flex items-center gap-2 text-white/50 hover:text-white transition-colors">
              View all <ChevronRight className="w-4 h-4" />
            </button>
          </div>
          <div className="grid grid-cols-3 gap-8">
            {trendingBrands.map((brand, index) => (
              <div
                key={brand.id}
                className="group relative aspect-[3/4] rounded-3xl overflow-hidden hover-trigger"
                style={{
                  transform: `translateY(${index * 40}px)`,
                }}
              >
                <video
                  loop
                  muted
                  playsInline
                  className="absolute inset-0 w-full h-full object-cover opacity-0 group-hover:opacity-100 transition-opacity duration-700"
                  onMouseEnter={(e) => (e.currentTarget as HTMLVideoElement).play()}
                  onMouseLeave={(e) => (e.currentTarget as HTMLVideoElement).pause()}
                >
                  <source src={brand.videoUrl} type="video/mp4" />
                </video>
                <img
                  src={brand.thumbnail}
                  alt={brand.name}
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-80" />
                
                {/* Brand Info */}
                <div className="absolute inset-x-0 bottom-0 p-8 transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
                  <div className="space-y-4">
                    <div className="flex items-center gap-4">
                      <span className="px-3 py-1 rounded-full bg-white/10 backdrop-blur-sm text-xs font-medium">
                        {brand.category}
                      </span>
                      <span className="text-white/70 text-sm">{brand.location}</span>
                    </div>
                    <h3 className="text-3xl font-bold">{brand.name}</h3>
                    <p className="text-white/70">{brand.description}</p>
                    <div className="flex items-center gap-6 pt-4">
                      <button className="flex items-center gap-2 px-6 py-3 bg-white text-black rounded-full font-medium hover:bg-white/90 transition-colors">
                        <Eye className="w-4 h-4" />
                        View Drop
                      </button>
                      <button className="p-3 rounded-full bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-colors">
                        <Share2 className="w-5 h-5" />
                      </button>
                      <button className="p-3 rounded-full bg-white/10 backdrop-blur-sm hover:bg-white/20 transition-colors">
                        <Heart className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>

                {/* Floating Stats */}
                <div className="absolute top-8 right-8 flex items-center gap-4 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                  <div className="glass-card px-4 py-2 rounded-full flex items-center gap-2">
                    <Users className="w-4 h-4" />
                    <span className="text-sm font-medium">
                      {(brand.followers / 1000000).toFixed(1)}M
                    </span>
                  </div>
                  <div className="glass-card px-4 py-2 rounded-full">
                    <span className="text-sm font-medium">
                      {brand.dropDate}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      {/* Floating Action Button */}
      <button className="fixed right-8 bottom-8 w-16 h-16 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full flex items-center justify-center hover:scale-110 transition-transform duration-300">
        <Plus className="w-8 h-8" />
      </button>
    </div>
  );
}

export default App;