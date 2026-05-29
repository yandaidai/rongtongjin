import React, { useCallback, useState } from 'react';
import {
  FlatList, RefreshControl, StyleSheet, Text, View,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { api } from '../api/client';
import QuoteCard from '../components/QuoteCard';
import Loading from '../components/Loading';
import type { MetalQuote } from '../types';

export default function DomesticQuotesScreen() {
  const [quotes, setQuotes] = useState<MetalQuote[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetch = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) setRefreshing(true);
      else setLoading(true);
      // 国内行情通过 /quotes/domestic 获取，但返回的是 MetalProductQuote
      // 这里用 /quotes/history 示例，实际需要调整
      const data = await api.getDomesticQuotes();
      // 转换为通用报价格式以显示大盘信息
      setQuotes(data.map((q) => ({
        id: q.product_id,
        product_id: q.product_id,
        price: q.market_price,
        open: null,
        high: null,
        low: null,
        rise: q.rise,
        rise_rate: q.rise_rate,
        quote_time: q.quote_time,
      })));
    } catch (e: any) {
      console.error('获取国内行情失败:', e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useFocusEffect(useCallback(() => { fetch(); }, [fetch]));

  if (loading && quotes.length === 0) return <Loading />;

  return (
    <View style={styles.container}>
      <FlatList
        data={quotes}
        keyExtractor={(item) => String(item.product_id)}
        renderItem={({ item }) => <QuoteCard quote={item} />}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => fetch(true)} />
        }
        contentContainerStyle={quotes.length === 0 ? styles.empty : undefined}
        ListEmptyComponent={<Text style={styles.emptyText}>暂无数据</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  empty: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  emptyText: { color: '#999', fontSize: 14 },
});
