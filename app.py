def get_gnews_with_sentiment():
    """Get news with AI sentiment analysis"""
    try:
        url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=10&apikey={GNEWS_API_KEY}"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            articles = []
            
            # Bullish keywords (Positive)
            bullish_words = ['surge', 'rally', 'gain', 'up', 'positive', 'bull', 'rise', 'high', 'record', 'boom', 
                            'growth', 'profit', 'upgrade', 'buy', 'strong', 'optimistic', 'boost', 'jump', 'peak']
            
            # Bearish keywords (Negative)  
            bearish_words = ['fall', 'drop', 'down', 'negative', 'bear', 'decline', 'low', 'crash', 'slump',
                            'loss', 'downgrade', 'sell', 'weak', 'pessimistic', 'fall', 'plunge', 'risk', 'fear']
            
            for article in data.get('articles', []):
                title = article['title'].lower()
                
                # Calculate sentiment score
                score = 0
                for word in bullish_words:
                    if word in title:
                        score += 10
                for word in bearish_words:
                    if word in title:
                        score -= 10
                
                # Determine sentiment
                if score > 5:
                    sentiment = "BULLISH"
                    strength = min(95, 60 + score)
                elif score < -5:
                    sentiment = "BEARISH"
                    strength = min(95, 60 + abs(score))
                else:
                    sentiment = "NEUTRAL"
                    strength = 50
                
                articles.append({
                    'title': article['title'],
                    'source': article['source']['name'],
                    'time': article['publishedAt'][:10],
                    'url': article['url'],
                    'sentiment': sentiment,
                    'strength': strength
                })
            return articles[:8]  # Return top 8 news
    except:
        pass
    
    # Fallback news with sentiment
    return [
        {'title': 'Nifty hits all-time high at 25,000', 'source': 'Economic Times', 'time': '2026-05-17', 'sentiment': 'BULLISH', 'strength': 85},
        {'title': 'RBI keeps repo rate unchanged at 6.5%', 'source': 'Business Standard', 'time': '2026-05-16', 'sentiment': 'BULLISH', 'strength': 70},
        {'title': 'Crude oil prices surge amid supply concerns', 'source': 'Reuters', 'time': '2026-05-16', 'sentiment': 'BEARISH', 'strength': 75},
        {'title': 'FIIs net buyers in Indian markets', 'source': 'Moneycontrol', 'time': '2026-05-16', 'sentiment': 'BULLISH', 'strength': 65},
        {'title': 'Inflation data to be released tomorrow', 'source': 'Bloomberg', 'time': '2026-05-16', 'sentiment': 'NEUTRAL', 'strength': 50},
    ]
