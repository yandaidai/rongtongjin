import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import type { MetalProductQuote } from '../types';

interface Props {
  quote: MetalProductQuote;
  onPress?: () => void;
}

export default function ProductCard({ quote, onPress }: Props) {
  const riseColor = quote.rise >= 0 ? '#e74c3c' : '#2ecc71';
  const arrow = quote.rise >= 0 ? '↑' : '↓';

  const Wrapper = onPress ? TouchableOpacity : View;

  return (
    <Wrapper style={styles.card} onPress={onPress} activeOpacity={0.7}>
      <View style={styles.header}>
        <Text style={styles.name}>{quote.product_name}</Text>
        <Text style={styles.code}>{quote.product_code}</Text>
      </View>

      <View style={styles.priceRow}>
        <Text style={styles.marketPrice}>¥{quote.market_price.toFixed(2)}</Text>
        <Text style={[styles.rise, { color: riseColor }]}>
          {arrow} {quote.rise_rate.toFixed(2)}%
        </Text>
      </View>

      <View style={styles.spreadRow}>
        <View style={styles.spreadItem}>
          <Text style={styles.spreadLabel}>销售价</Text>
          <Text style={styles.spreadValue}>¥{quote.sell_price.toFixed(2)}</Text>
        </View>
        <View style={styles.divider} />
        <View style={styles.spreadItem}>
          <Text style={styles.spreadLabel}>回购价</Text>
          <Text style={styles.spreadValue}>¥{quote.buy_back_price.toFixed(2)}</Text>
        </View>
      </View>
    </Wrapper>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  name: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1a1a2e',
  },
  code: {
    fontSize: 12,
    color: '#999',
  },
  priceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'baseline',
    marginBottom: 12,
  },
  marketPrice: {
    fontSize: 28,
    fontWeight: '700',
    color: '#1a1a2e',
  },
  rise: {
    fontSize: 14,
    fontWeight: '600',
  },
  spreadRow: {
    flexDirection: 'row',
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 10,
  },
  spreadItem: {
    flex: 1,
    alignItems: 'center',
  },
  spreadLabel: {
    fontSize: 12,
    color: '#999',
    marginBottom: 2,
  },
  spreadValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#d4a84b',
  },
  divider: {
    width: 1,
    backgroundColor: '#e0e0e0',
    marginHorizontal: 8,
  },
});
