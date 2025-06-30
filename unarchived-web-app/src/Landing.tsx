import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles, Globe, Users, TrendingUp, Star, PlayCircle, ArrowUpRight, Book, Newspaper, Lightbulb } from 'lucide-react';

const LandingPage = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const brandHighlights = [
    {
      id: 1,
      name: "ACRONYM",
      image: "https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?auto=format&fit=crop&w=600&q=80",
      category: "TECH WEAR",
      followers: "1.2M",
      engagement: "97%"
    },
    {
      id: 2,
      name: "NEURAL",
      image: "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=600&q=80",
      category: "AI FASHION",
      followers: "2.5M",
      engagement: "94%"
    },
    {
      id: 3,
      name: "VOID",
      image: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=600&q=80",
      category: "AVANT-GARDE",
      followers: "800K",
      engagement: "92%"
    }
  ];

  const stats = [
    { value: "2M+", label: "Active Users" },
    { value: "10K+", label: "Verified Brands" },
    { value: "500+", label: "Daily Drops" },
    { value: "98%", label: "User Satisfaction" }
  ];

  const features = [
    {
      icon: Globe,
      title: "Global Reach",
      description: "Connect with fashion enthusiasts and brands worldwide"
    },
    {
      icon: Users,
      title: "Community First",
      description: "Join exclusive brand communities and discussions"
    },
    {
      icon: TrendingUp,
      title: "Trend Analysis",
      description: "Stay ahead with AI-powered trend predictions"
    },
    {
      icon: Star,
      title: "Exclusive Drops",
      description: "Get early access to limited edition releases"
    }
  ];

  return (
    <div className="min-h-screen text-white">
      {/* Custom Cursor */}
      <div
        className={`custom-cursor fixed w-6 h-6 bg-white rounded-full pointer-events-none z-50 ${
          isHovering ? 'hover' : ''
        }`}
        style={{
          transform: `translate(${mousePosition.x - 12}px, ${mousePosition.y - 12}px)`,
        }}
      />

      {/* Enhanced Navigation */}
      <nav className="fixed top-0 left-0 right-0 flex justify-between items-center py-6 px-12 bg-black/20 backdrop-blur-lg z-40">
        <div className="flex items-center gap-2">
          <div className="w-12 h-12 bg-gradient-to-br from-white/20 to-white/5 backdrop-blur-lg rounded-xl flex items-center justify-center">
            <span className="text-xl font-bold">UN</span>
          </div>
          <span className="text-2xl font-bold tracking-tighter">UNARCHIVED</span>
        </div>

        <div className="flex items-center gap-12">
          <div className="flex items-center gap-8">
            {[
              { label: 'Features', items: ['For Brands', 'For Creators', 'For Users'] },
              { label: 'Resources', items: ['Blog', 'Guides', 'Case Studies'] },
              { label: 'Updates', items: ['Changelog', 'Roadmap', 'Status'] },
            ].map((menu) => (
              <div
                key={menu.label}
                className="relative group"
                onMouseEnter={() => setIsHovering(true)}
                onMouseLeave={() => setIsHovering(false)}
              >
                <button className="px-4 py-2 rounded-lg hover:bg-white/5 transition-colors link-hover">
                  {menu.label}
                </button>
                <div className="absolute top-full left-1/2 -translate-x-1/2 pt-4 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  <div className="bg-white/10 backdrop-blur-lg rounded-xl p-2 min-w-[160px]">
                    {menu.items.map((item) => (
                      <button
                        key={item}
                        className="w-full text-left px-4 py-2 rounded-lg hover:bg-white/5 transition-colors text-sm"
                      >
                        {item}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="flex items-center gap-4">
            <Link
              to="/login"
              className="px-6 py-2 rounded-full hover:bg-white/5 transition-colors"
              onMouseEnter={() => setIsHovering(true)}
              onMouseLeave={() => setIsHovering(false)}
            >
              Log in
            </Link>
            <Link
              to="/signup"
              className="px-6 py-2 bg-white text-black rounded-full hover:bg-white/90 transition-colors"
              onMouseEnter={() => setIsHovering(true)}
              onMouseLeave={() => setIsHovering(false)}
            >
              Sign up
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 to-black z-10" />
        <video
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-cover"
        >
          <source src="https://assets.mixkit.co/videos/preview/mixkit-fashion-model-walking-on-wooden-floor-34744-large.mp4" type="video/mp4" />
        </video>
        
        <div className="relative z-20 container mx-auto px-6 py-24">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <h1 className="text-7xl font-bold leading-tight">
              The Social Network for
              <span className="block bg-clip-text text-transparent bg-gradient-to-r from-white via-white/50 to-white">
                Fashion Discovery
              </span>
            </h1>
            <p className="text-xl text-white/70">
              Connect with emerging brands, discover exclusive drops, and be part of the next generation of fashion culture.
            </p>
            <div className="flex items-center justify-center gap-6 pt-8">
              <button className="px-8 py-4 bg-white text-black rounded-full font-medium hover:bg-white/90 transition-colors flex items-center gap-2">
                Get Started <ArrowRight className="w-5 h-5" />
              </button>
              <button className="px-8 py-4 bg-white/10 backdrop-blur-sm rounded-full font-medium hover:bg-white/20 transition-colors flex items-center gap-2">
                Watch Demo <PlayCircle className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="absolute bottom-12 left-1/2 -translate-x-1/2">
            <div className="grid grid-cols-4 gap-12 px-12 py-6 bg-white/5 backdrop-blur-lg rounded-2xl">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl font-bold">{stat.value}</div>
                  <div className="text-sm text-white/70">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Brand Highlights Section */}
      <section className="py-24 relative">
        <div className="container mx-auto px-6">
          <div className="flex items-end justify-between mb-16">
            <div>
              <h2 className="text-4xl font-bold mb-4">Brand Highlights</h2>
              <p className="text-white/70 max-w-xl">
                Discover trending brands that are reshaping the fashion landscape through innovation and creativity.
              </p>
            </div>
            <button className="flex items-center gap-2 text-white/50 hover:text-white transition-colors">
              View All Brands <ArrowUpRight className="w-5 h-5" />
            </button>
          </div>

          <div className="grid grid-cols-3 gap-8">
            {brandHighlights.map((brand, index) => (
              <div
                key={brand.id}
                className="group relative aspect-[3/4] rounded-3xl overflow-hidden"
                style={{
                  transform: `translateY(${index * 40}px)`,
                }}
              >
                <img
                  src={brand.image}
                  alt={brand.name}
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />
                
                <div className="absolute inset-x-0 bottom-0 p-8">
                  <div className="space-y-4">
                    <div className="flex items-center gap-4">
                      <span className="px-3 py-1 rounded-full bg-white/10 backdrop-blur-sm text-xs font-medium">
                        {brand.category}
                      </span>
                    </div>
                    <h3 className="text-3xl font-bold">{brand.name}</h3>
                    <div className="flex items-center gap-4 text-sm text-white/70">
                      <span>{brand.followers} Followers</span>
                      <span>{brand.engagement} Engagement</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 relative">
        <div className="container mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-20">
            <h2 className="text-4xl font-bold mb-6">Redefining Fashion Discovery</h2>
            <p className="text-white/70">
              Experience fashion like never before with our innovative platform that connects brands, creators, and enthusiasts in one unified space.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-12">
            {features.map((feature, index) => (
              <div key={index} className="group p-8 rounded-3xl bg-white/5 hover:bg-white/10 transition-colors">
                <feature.icon className="w-12 h-12 mb-6" />
                <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
                <p className="text-white/70">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Community Section */}
      <section className="py-24 relative">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-2 gap-24 items-center">
            <div>
              <h2 className="text-4xl font-bold mb-8">Join Our Growing Community</h2>
              <p className="text-white/70 mb-8">
                Be part of a vibrant community of fashion enthusiasts, designers, and brands. Share your style, discover new trends, and connect with like-minded individuals from around the world.
              </p>
              <div className="space-y-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center">
                    <Sparkles className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold mb-1">Curated Content</h3>
                    <p className="text-white/70">Personalized feed based on your interests</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center">
                    <Users className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold mb-1">Exclusive Events</h3>
                    <p className="text-white/70">Virtual and physical fashion events</p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center">
                    <Star className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold mb-1">Early Access</h3>
                    <p className="text-white/70">Be first to know about new drops</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="relative aspect-square">
              <img
                src="https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=800&q=80"
                alt="Community"
                className="rounded-3xl object-cover w-full h-full"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent rounded-3xl" />
              <div className="absolute bottom-8 left-8 right-8 p-6 bg-white/10 backdrop-blur-lg rounded-2xl">
                <div className="flex items-center gap-4 mb-4">
                  <div className="flex -space-x-4">
                    <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=64&h=64&q=80" alt="User" className="w-10 h-10 rounded-full border-2 border-black" />
                    <img src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=64&h=64&q=80" alt="User" className="w-10 h-10 rounded-full border-2 border-black" />
                    <img src="https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=64&h=64&q=80" alt="User" className="w-10 h-10 rounded-full border-2 border-black" />
                  </div>
                  <div className="text-sm">
                    <p className="font-bold">Join 2M+ members</p>
                    <p className="text-white/70">Growing every day</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;