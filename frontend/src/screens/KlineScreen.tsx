import React, { useCallback, useState } from 'react';
import {
  FlatList, RefreshControl, ScrollView, StyleSheet, Text, TouchableOpacity, View,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { api } from '../api/client';
import KlineChart from '../components/KlineChart';
import Loading from '../components/Loading';
import type { MetalKline } from '../types';

const K_TYPES = [
  { key: 'minute', label: '分钟' },
  { key: 'two_day', label: '两日' },
  { key: 'day', label: '日K' },
  { key: 'week', label: '周K' },
  { key: 'month', label: '月K' },
];

export default function KlineScreen({ route, navigation }: any) {
  const { productId, productCode, productName } = route.params;
  const [kType, setKType] = useState('minute');
  const [klines, setKlines] = useState<MetalKline[]>([]);
  const [latest, setLatest] = useState<MetalKline[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetch = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) setRefreshing(true);
      else setLoading(true);
      const [kData, latestData] = await Promise.all([
        api.getKlines(productId, kType),
        api.getLatestKlines(productId, kType, 10),
      ]);
      setKlines(kData);
      setLatest(latestData);
    } catch (e: any) {
      console.error('获取K线失败:', e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [productId, kType]);

  useFocusEffect(useCallback(() => { fetch(); }, [fetch]));

  if (loading && klines.length === 0) return <Loading />;

  return (
    <ScrollView style={styles.container} refreshControl={
      <RefreshControl refreshing={refreshing} onRefresh={() => fetch(true)} />
    }>
      <View style={styles.header}>
        <Text style={styles.title}>{productName} ({productCode})</Text>
      </View>

      {/* K 线类型切换 */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.kTypeRow}>
        {K_TYPES.map((t) => (
          <TouchableOpacity
            key={t.key}
            style={[styles.kTypeBtn, kType === t.key && styles.kTypeBtnActive]}
            onPress={() => setKType(t.key)}
          >
            <Text style={[styles.kTypeText, kType === t.key && styles.kTypeTextActive]}>
              {t.label}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* K 线图 */}
      <KlineChart data={klines} title={`${productName} ${K_TYPES.find(t => t.key === kType)?.label}`} />

      {/* 最新价格记录 */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>最新价格记录</Text>
        {latest.map((k, i) => (
          <View key={k.id || i} style={styles.recordRow}>
            <Text style={styles.recordTime}>
              {new Date(k.k_time).toLocaleString('zh-CN')}
            </Text>
            <Text style={styles.recordPrice}>¥{k.close_price.toFixed(2)}</Text>
          </View>
        ))}
      </View>

      {/* 提醒设置入口 */}
      <TouchableOpacity
        style={styles.warnBtn}
        onPress={() => navigation.navigate('WarnCreate', {
          productId,
          productName,
        })}
      >
        <Text style={styles.warnBtnText}>设置价格提醒</Text>
      </TouchableOpacity>

      <View style={{ height: 40 }} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { paddingHorizontal: 16, paddingTop: 12 },
  title: { fontSize: 18, fontWeight: '700', color: '#1a1a2e' },
  kTypeRow: { paddingHorizontal: 16, marginTop: 12, marginBottom: 4 },
  kTypeBtn: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#fff',
    marginRight: 8,
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 4,
    elevation: 1,
  },
  kTypeBtnActive: { backgroundColor: '#d4a84b' },
  kTypeText: { fontSize: 13, color: '#666' },
  kTypeTextActive: { color: '#fff', fontWeight: '600' },
  section: { backgroundColor: '#fff', borderRadius: 12, margin: 16, marginBottom: 0, padding: 16 },
  sectionTitle: { fontSize: 15, fontWeight: '700', color: '#1a1a2e', marginBottom: 10 },
  recordRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  recordTime: { fontSize: 13, color: '#666' },
  recordPrice: { fontSize: 14, fontWeight: '600', color: '#1a1a2e' },
  warnBtn: {
    backgroundColor: '#d4a84b',
    borderRadius: 10,
    padding: 14,
    margin: 16,
    alignItems: 'center',
  },
  warnBtnText: { color: '#fff', fontSize: 15, fontWeight: '700' },
});
