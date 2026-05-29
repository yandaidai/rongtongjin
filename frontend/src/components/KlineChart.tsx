import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import type { MetalKline } from '../types';

interface Props {
  data: MetalKline[];
  title?: string;
}

export default function KlineChart({ data, title }: Props) {
  if (data.length === 0) {
    return (
      <View style={styles.empty}>
        <Text style={styles.emptyText}>暂无数据</Text>
      </View>
    );
  }

  const prices = data.map((k) => k.close_price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const range = max - min || 1;
  const latest = prices[prices.length - 1];
  const prev = prices.length > 1 ? prices[prices.length - 2] : latest;
  const diff = latest - prev;
  const diffRate = prev !== 0 ? ((diff / prev) * 100).toFixed(2) : '0.00';
  const riseColor = diff >= 0 ? '#e74c3c' : '#2ecc71';

  return (
    <View style={styles.container}>
      {title && <Text style={styles.title}>{title}</Text>}

      {/* 当前价格 */}
      <View style={styles.priceHeader}>
        <Text style={[styles.latestPrice, { color: riseColor }]}>
          ¥{latest.toFixed(2)}
        </Text>
        <Text style={[styles.diff, { color: riseColor }]}>
          {diff >= 0 ? '+' : ''}{diff.toFixed(2)} ({diffRate}%)
        </Text>
      </View>

      {/* 高低价 */}
      <View style={styles.rangeRow}>
        <Text style={styles.rangeLabel}>高 {max.toFixed(2)}</Text>
        <Text style={styles.rangeLabel}>低 {min.toFixed(2)}</Text>
      </View>

      {/* 简化折线图 */}
      <View style={styles.chart}>
        {prices.map((p, i) => {
          const height = ((p - min) / range) * 120;
          return (
            <View
              key={i}
              style={[
                styles.bar,
                {
                  height: Math.max(height, 2),
                  backgroundColor: p >= (prices[i - 1] ?? p) ? '#e74c3c' : '#2ecc71',
                },
              ]}
            />
          );
        })}
      </View>

      {/* 开盘/收盘标签 */}
      <View style={styles.rangeRow}>
        <Text style={styles.rangeLabel}>
          开 {data[0]?.open_price.toFixed(2)}
        </Text>
        <Text style={styles.rangeLabel}>
          昨收 {data[0]?.close_price.toFixed(2)}
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.08,
    shadowRadius: 8,
    elevation: 3,
  },
  title: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1a1a2e',
    marginBottom: 8,
  },
  priceHeader: {
    flexDirection: 'row',
    alignItems: 'baseline',
    gap: 8,
  },
  latestPrice: {
    fontSize: 28,
    fontWeight: '700',
  },
  diff: {
    fontSize: 14,
    fontWeight: '600',
  },
  rangeRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 4,
    marginBottom: 8,
  },
  rangeLabel: {
    fontSize: 12,
    color: '#999',
  },
  chart: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    height: 130,
    gap: 1,
    paddingVertical: 4,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  bar: {
    flex: 1,
    borderRadius: 1,
    minWidth: 2,
  },
  empty: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    color: '#999',
    fontSize: 14,
  },
});
