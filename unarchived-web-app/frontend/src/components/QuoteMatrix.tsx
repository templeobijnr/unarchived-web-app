import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Check, Clock, MapPin, Award, Star } from 'lucide-react';
import { formatCurrency } from '@/lib/utils';
import { mockQuotes } from '@/lib/mockData';

interface QuoteMatrixProps {
  quotes?: typeof mockQuotes;
  onSelectQuote?: (quoteId: string) => void;
}

const QuoteMatrix = ({ quotes = mockQuotes.slice(0, 3), onSelectQuote }: QuoteMatrixProps) => {
  const [selectedCurrency, setSelectedCurrency] = useState<'USD' | 'EUR' | 'CNY'>('USD');
  const [selectedQuote, setSelectedQuote] = useState<string | null>(null);

  const currencyRates = {
    USD: 1,
    EUR: 0.85,
    CNY: 7.2
  };

  const convertPrice = (price: number, fromCurrency: string) => {
    if (fromCurrency === selectedCurrency) return price;
    const usdPrice = fromCurrency === 'USD' ? price : price / currencyRates[fromCurrency as keyof typeof currencyRates];
    return usdPrice * currencyRates[selectedCurrency];
  };

  const handleSelectQuote = (quoteId: string) => {
    setSelectedQuote(quoteId);
    onSelectQuote?.(quoteId);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-2xl font-bold text-text-primary">Quote Comparison</h3>
          <p className="text-text-secondary">Compare supplier offers side by side</p>
        </div>
        <div className="flex items-center space-x-2">
          {(['USD', 'EUR', 'CNY'] as const).map((currency) => (
            <Button
              key={currency}
              variant={selectedCurrency === currency ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedCurrency(currency)}
            >
              {currency}
            </Button>
          ))}
        </div>
      </div>

      {/* Quote Cards */}
      <div className="grid md:grid-cols-3 gap-6">
        {quotes.map((quote, index) => (
          <motion.div
            key={quote.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Card className={`relative h-full transition-all duration-300 hover:shadow-2xl ${
              selectedQuote === quote.id ? 'ring-2 ring-accent-gradient-from' : ''
            }`}>
              {/* Best Value Badge */}
              {index === 1 && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 z-10">
                  <Badge className="bg-gradient-accent text-white px-3 py-1">
                    <Star className="w-3 h-3 mr-1" />
                    Best Value
                  </Badge>
                </div>
              )}

              <CardHeader className="text-center pb-4">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full overflow-hidden">
                  <img 
                    src={quote.supplierLogo} 
                    alt={quote.supplierName}
                    className="w-full h-full object-cover"
                  />
                </div>
                <CardTitle className="text-lg">{quote.supplierName}</CardTitle>
                <div className="flex items-center justify-center space-x-1 text-sm text-text-secondary">
                  <MapPin className="w-4 h-4" />
                  <span>China</span>
                </div>
              </CardHeader>

              <CardContent className="space-y-4">
                {/* Price */}
                <div className="text-center p-4 glass-effect rounded-lg">
                  <div className="text-3xl font-bold text-text-primary">
                    {formatCurrency(convertPrice(quote.price, quote.currency), selectedCurrency)}
                  </div>
                  <div className="text-sm text-text-secondary">per unit</div>
                  <div className="text-xs text-text-secondary mt-1">
                    MOQ: {quote.moq.toLocaleString()} units
                  </div>
                </div>

                {/* Specs */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-text-secondary">Lead Time</span>
                    <div className="flex items-center space-x-1">
                      <Clock className="w-4 h-4 text-text-accent" />
                      <span className="text-text-primary">{quote.leadTime} days</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-text-secondary">Material</span>
                    <span className="text-text-primary">{quote.specs.material}</span>
                  </div>
                  
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-text-secondary">Printing</span>
                    <span className="text-text-primary">{quote.specs.printing}</span>
                  </div>
                </div>

                {/* Features */}
                <div className="space-y-2">
                  <div className="flex items-center space-x-2 text-sm">
                    <Check className="w-4 h-4 text-success" />
                    <span className="text-text-primary">Quality assurance</span>
                  </div>
                  <div className="flex items-center space-x-2 text-sm">
                    <Check className="w-4 h-4 text-success" />
                    <span className="text-text-primary">Escrow protection</span>
                  </div>
                  <div className="flex items-center space-x-2 text-sm">
                    <Award className="w-4 h-4 text-text-accent" />
                    <span className="text-text-primary">Verified supplier</span>
                  </div>
                </div>

                {/* Action Button */}
                <Button 
                  className="w-full"
                  variant={selectedQuote === quote.id ? 'secondary' : 'default'}
                  onClick={() => handleSelectQuote(quote.id)}
                >
                  {selectedQuote === quote.id ? 'Selected' : 'Select Supplier'}
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Summary */}
      {selectedQuote && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-6 glass-effect rounded-lg border border-surface-border"
        >
          <h4 className="font-semibold text-text-primary mb-2">Next Steps</h4>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-full bg-gradient-accent text-white flex items-center justify-center text-xs">1</div>
              <span className="text-text-secondary">Sample approval</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-full bg-surface-glass text-text-primary flex items-center justify-center text-xs">2</div>
              <span className="text-text-secondary">Deposit via escrow</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 rounded-full bg-surface-glass text-text-primary flex items-center justify-center text-xs">3</div>
              <span className="text-text-secondary">Production starts</span>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default QuoteMatrix;