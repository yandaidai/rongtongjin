import React, { useCallback, useState } from 'react';
import {
  Alert, FlatList, RefreshControl, StyleSheet, Switch, Text, TouchableOpacity, View,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { api } from '../api/client';
import Loading from '../components/Loading';
import type { MetalWarn } from '../types';

export default function WarnListScreen({ navigation }: any) {
  const [warns, setWarns] = useState<MetalWarn[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetch = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) setRefreshing(true);
      else setLoading(true);
      const data = await api.getUserWarns();
      setWarns(data);
    } catch (e: any) {
      console.error('获取预警失败:', e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useFocusEffect(useCallback(() => { fetch(); }, [fetch]));

  const toggleWarn = async (warn: MetalWarn) => {
    try {
      await api.updateWarn(warn.id, { warn_enable: !warn.warn_enable });
      fetch(true);
    } catch (e: any) {
      Alert.alert('失败', e.message);
    }
  };

  const deleteWarn = (warn: MetalWarn) => {
    Alert.alert('删除预警', '确定删除该预警配置？', [
      { text: '取消', style: 'cancel' },
      {
        text: '删除',
        style: 'destructive',
        onPress: async () => {
          try {
            await api.deleteWarn(warn.id);
            fetch(true);
          } catch (e: any) {
            Alert.alert('失败', e.message);
          }
        },
      },
    ]);
  };

  if (loading && warns.length === 0) return <Loading />;

  return (
    <View style={styles.container}>
      <FlatList
        data={warns}
        keyExtractor={(item) => String(item.id)}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => fetch(true)} />
        }
        renderItem={({ item }) => (
          <View style={styles.card}>
            <View style={styles.cardHeader}>
              <Text style={styles.productLabel}>品种 #{item.product_id}</Text>
              <Switch
                value={item.warn_enable}
                onValueChange={() => toggleWarn(item)}
                trackColor={{ false: '#ddd', true: '#d4a84b' }}
                thumbColor="#fff"
              />
            </View>

            <View style={styles.limitRow}>
              <View style={styles.limitItem}>
                <Text style={styles.limitLabel}>最高阀值</Text>
                <Text style={styles.limitValue}>
                  {item.upper_limit != null ? `¥${item.upper_limit}` : '未设置'}
                </Text>
                {item.upper_trigger && (
                  <Text style={styles.triggered}>已触发</Text>
                )}
              </View>
              <View style={styles.limitItem}>
                <Text style={styles.limitLabel}>最低阀值</Text>
                <Text style={styles.limitValue}>
                  {item.lower_limit != null ? `¥${item.lower_limit}` : '未设置'}
                </Text>
                {item.lower_trigger && (
                  <Text style={styles.triggered}>已触发</Text>
                )}
              </View>
            </View>

            <View style={styles.actionRow}>
              <TouchableOpacity
                style={styles.editBtn}
                onPress={() => navigation.navigate('WarnCreate', {
                  warnId: item.id,
                  productId: item.product_id,
                  upperLimit: item.upper_limit,
                  lowerLimit: item.lower_limit,
                })}
              >
                <Text style={styles.editBtnText}>编辑</Text>
              </TouchableOpacity>
              <TouchableOpacity onPress={() => deleteWarn(item)}>
                <Text style={styles.deleteBtnText}>删除</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text style={styles.emptyText}>暂无预警配置</Text>
            <TouchableOpacity
              style={styles.addBtn}
              onPress={() => navigation.navigate('WarnCreate', {})}
            >
              <Text style={styles.addBtnText}>添加预警</Text>
            </TouchableOpacity>
          </View>
        }
      />

      {/* 浮动添加按钮 */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => navigation.navigate('WarnCreate', {})}
      >
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    margin: 16,
    marginBottom: 0,
    padding: 16,
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  productLabel: { fontSize: 15, fontWeight: '700', color: '#1a1a2e' },
  limitRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 10,
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
  },
  limitItem: { alignItems: 'center' },
  limitLabel: { fontSize: 12, color: '#999', marginBottom: 4 },
  limitValue: { fontSize: 16, fontWeight: '700', color: '#1a1a2e' },
  triggered: { fontSize: 11, color: '#e74c3c', marginTop: 2, fontWeight: '600' },
  actionRow: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    gap: 16,
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
    paddingTop: 10,
  },
  editBtn: {},
  editBtnText: { color: '#d4a84b', fontWeight: '600' },
  deleteBtnText: { color: '#e74c3c', fontWeight: '600' },
  empty: { alignItems: 'center', paddingTop: 60 },
  emptyText: { color: '#999', fontSize: 14, marginBottom: 16 },
  addBtn: { backgroundColor: '#d4a84b', borderRadius: 8, paddingHorizontal: 24, paddingVertical: 10 },
  addBtnText: { color: '#fff', fontWeight: '600' },
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 30,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#d4a84b',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 5,
  },
  fabText: { color: '#fff', fontSize: 28, fontWeight: '300', marginTop: -2 },
});
