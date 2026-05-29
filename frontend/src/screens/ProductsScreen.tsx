import React, { useCallback, useState } from 'react';
import {
  FlatList, RefreshControl, StyleSheet, Text, View,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { api } from '../api/client';
import ProductCard from '../components/ProductCard';
import Loading from '../components/Loading';
import type { MetalProductQuote } from '../types';

export default function ProductsScreen({ navigation }: any) {
  const [quotes, setQuotes] = useState<MetalProductQuote[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetch = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) setRefreshing(true);
      else setLoading(true);
      const data = await api.getQuotes();
      setQuotes(data);
    } catch (e: any) {
      console.error('获取行情失败:', e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useFocusEffect(useCallback(() => { fetch(); }, [fetch]));

  const handlePress = (quote: MetalProductQuote) => {
    navigation.navigate('Kline', {
      productId: quote.product_id,
      productCode: quote.product_code,
      productName: quote.product_name,
    });
  };

  if (loading && quotes.length === 0) return <Loading />;

  return (
    <View style={styles.container}>
      <FlatList
        data={quotes}
        keyExtractor={(item) => String(item.product_id)}
        renderItem={({ item }) => (
          <ProductCard quote={item} onPress={() => handlePress(item)} />
        )}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => fetch(true)} />
        }
        contentContainerStyle={quotes.length === 0 ? styles.empty : undefined}
        ListEmptyComponent={
          <Text style={styles.emptyText}>暂无行情数据，下拉刷新</Text>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  empty: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  emptyText: { color: '#999', fontSize: 14 },
});
