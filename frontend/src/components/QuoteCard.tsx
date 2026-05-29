import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import type { MetalQuote } from '../types';

interface Props {
  quote: MetalQuote;
}

export default function QuoteCard({ quote }: Props) {
  const riseColor = quote.rise >= 0 ? '#e74c3c' : '#2ecc71';
  const arrow = quote.rise >= 0 ? '↑' : '↓';

  return (
    <View style={styles.card}>
      <View style={styles.priceRow}>
        <Text style={styles.price}>¥{quote.price.toFixed(2)}</Text>
        <View style={styles.changeInfo}>
          <Text style={[styles.rise, { color: riseColor }]}>
            {arrow} {quote.rise.toFixed(2)}
          </Text>
          <Text style={[styles.riseRate, { color: riseColor }]}>
            {quote.rise_rate.toFixed(2)}%
          </Text>
        </View>
      </View>
      {quote.open != null && (
        <View style={styles.detailRow}>
          <Text style={styles.detail}>开 {quote.open.toFixed(2)}</Text>
          <Text style={styles.detail}>高 {quote.high?.toFixed(2)}</Text>
          <Text style={styles.detail}>低 {quote.low?.toFixed(2)}</Text>
        </View>
      )}
      <Text style={styles.time}>
        {new Date(quote.quote_time).toLocaleString('zh-CN')}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 14,
    marginHorizontal: 16,
    marginVertical: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  priceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  price: {
    fontSize: 22,
    fontWeight: '700',
    color: '#1a1a2e',
  },
  changeInfo: {
    alignItems: 'flex-end',
  },
  rise: {
    fontSize: 14,
    fontWeight: '600',
  },
  riseRate: {
    fontSize: 12,
    marginTop: 2,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 8,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
  },
  detail: {
    fontSize: 12,
    color: '#666',
  },
  time: {
    fontSize: 10,
    color: '#bbb',
    marginTop: 6,
    textAlign: 'right',
  },
});
