import React, { useCallback, useState } from 'react';
import {
  Alert, FlatList, RefreshControl, StyleSheet, Text, TextInput, TouchableOpacity, View,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { api } from '../api/client';
import Loading from '../components/Loading';
import type { MetalProduct, UserConfig } from '../types';

export default function SpreadConfigScreen() {
  const [products, setProducts] = useState<MetalProduct[]>([]);
  const [userConfigs, setUserConfigs] = useState<UserConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [editingProduct, setEditingProduct] = useState<number | null>(null);
  const [sellAdd, setSellAdd] = useState('');
  const [buyBackSub, setBuyBackSub] = useState('');

  const fetch = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) setRefreshing(true);
      else setLoading(true);
      const [p, c] = await Promise.all([
        api.getProducts(),
        api.getUserConfigs(),
      ]);
      setProducts(p);
      setUserConfigs(c);
    } catch (e: any) {
      console.error('获取配置失败:', e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useFocusEffect(useCallback(() => { fetch(); }, [fetch]));

  const getConfigForProduct = (productId: number) =>
    userConfigs.find((c) => c.product_id === productId);

  const handleEdit = (productId: number) => {
    const config = getConfigForProduct(productId);
    setSellAdd(config ? String(config.sell_add_price) : '');
    setBuyBackSub(config ? String(config.buy_back_sub_price) : '');
    setEditingProduct(productId);
  };

  const handleSave = async () => {
    if (editingProduct === null) return;
    const sell = parseFloat(sellAdd);
    const buy = parseFloat(buyBackSub);
    if (isNaN(sell) || isNaN(buy)) {
      Alert.alert('提示', '请输入有效的数值');
      return;
    }
    try {
      await api.upsertUserConfig({
        product_id: editingProduct,
        sell_add_price: sell,
        buy_back_sub_price: buy,
      });
      Alert.alert('成功', '点差配置已更新');
      setEditingProduct(null);
      fetch(true);
    } catch (e: any) {
      Alert.alert('失败', e.message);
    }
  };

  if (loading && products.length === 0) return <Loading />;

  return (
    <View style={styles.container}>
      <FlatList
        data={products}
        keyExtractor={(item) => String(item.id)}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => fetch(true)} />
        }
        renderItem={({ item }) => {
          const config = getConfigForProduct(item.id);
          const isEditing = editingProduct === item.id;

          return (
            <View style={styles.card}>
              <View style={styles.cardHeader}>
                <Text style={styles.productName}>{item.name}</Text>
                <Text style={styles.productCode}>{item.code}</Text>
              </View>

              {isEditing ? (
                <View>
                  <View style={styles.inputRow}>
                    <Text style={styles.inputLabel}>销售价加点</Text>
                    <TextInput
                      style={styles.input}
                      value={sellAdd}
                      onChangeText={setSellAdd}
                      keyboardType="decimal-pad"
                      placeholder="默认 3.0"
                    />
                  </View>
                  <View style={styles.inputRow}>
                    <Text style={styles.inputLabel}>回购价减点</Text>
                    <TextInput
                      style={styles.input}
                      value={buyBackSub}
                      onChangeText={setBuyBackSub}
                      keyboardType="decimal-pad"
                      placeholder="默认 2.0"
                    />
                  </View>
                  <View style={styles.btnRow}>
                    <TouchableOpacity style={styles.saveBtn} onPress={handleSave}>
                      <Text style={styles.saveBtnText}>保存</Text>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={() => setEditingProduct(null)}>
                      <Text style={styles.cancelBtn}>取消</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              ) : (
                <View>
                  <View style={styles.configRow}>
                    <Text style={styles.configLabel}>销售价加点</Text>
                    <Text style={styles.configValue}>
                      +{config?.sell_add_price ?? 3.0} 元/克
                    </Text>
                  </View>
                  <View style={styles.configRow}>
                    <Text style={styles.configLabel}>回购价减点</Text>
                    <Text style={styles.configValue}>
                      -{config?.buy_back_sub_price ?? 2.0} 元/克
                    </Text>
                  </View>
                  <TouchableOpacity style={styles.editBtn} onPress={() => handleEdit(item.id)}>
                    <Text style={styles.editBtnText}>自定义</Text>
                  </TouchableOpacity>
                </View>
              )}
            </View>
          );
        }}
        ListEmptyComponent={
          <Text style={styles.emptyText}>暂无品种数据</Text>
        }
      />
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
    marginBottom: 10,
  },
  productName: { fontSize: 16, fontWeight: '700', color: '#1a1a2e' },
  productCode: { fontSize: 13, color: '#999' },
  configRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 6,
  },
  configLabel: { fontSize: 14, color: '#666' },
  configValue: { fontSize: 14, fontWeight: '600', color: '#d4a84b' },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  inputLabel: { fontSize: 14, color: '#333' },
  input: {
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    padding: 8,
    width: 120,
    textAlign: 'right',
    fontSize: 14,
  },
  btnRow: { flexDirection: 'row', justifyContent: 'flex-end', gap: 12, marginTop: 8 },
  saveBtn: { backgroundColor: '#d4a84b', borderRadius: 8, paddingHorizontal: 20, paddingVertical: 10 },
  saveBtnText: { color: '#fff', fontWeight: '600' },
  cancelBtn: { color: '#999', fontSize: 14, paddingVertical: 10 },
  editBtn: { alignSelf: 'flex-end', marginTop: 8 },
  editBtnText: { color: '#d4a84b', fontWeight: '600', fontSize: 14 },
  emptyText: { textAlign: 'center', color: '#999', marginTop: 40 },
});
