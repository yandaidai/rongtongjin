import React, { useCallback, useState } from 'react';
import {
  Alert, ScrollView, StyleSheet, Switch, Text, TextInput, TouchableOpacity, View,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { api } from '../api/client';
import Loading from '../components/Loading';
import type { MetalProduct } from '../types';

export default function WarnCreateScreen({ route, navigation }: any) {
  const { warnId, productId: editProductId, upperLimit: editUpper, lowerLimit: editLower } = route.params || {};
  const isEdit = !!warnId;

  const [products, setProducts] = useState<MetalProduct[]>([]);
  const [productId, setProductId] = useState<number | null>(editProductId || null);
  const [upperLimit, setUpperLimit] = useState(editUpper != null ? String(editUpper) : '');
  const [lowerLimit, setLowerLimit] = useState(editLower != null ? String(editLower) : '');
  const [warnEnable, setWarnEnable] = useState(true);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useFocusEffect(useCallback(() => {
    api.getProducts()
      .then(setProducts)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []));

  const handleSave = async () => {
    if (!productId) {
      Alert.alert('提示', '请选择品种');
      return;
    }
    if (!upperLimit && !lowerLimit) {
      Alert.alert('提示', '请至少设置一个阀值');
      return;
    }

    setSaving(true);
    try {
      const data = {
        product_id: productId,
        upper_limit: upperLimit ? parseFloat(upperLimit) : null,
        lower_limit: lowerLimit ? parseFloat(lowerLimit) : null,
        warn_enable: warnEnable,
      };

      if (isEdit) {
        await api.updateWarn(warnId, data);
      } else {
        await api.createWarn(data);
      }
      Alert.alert('成功', isEdit ? '预警已更新' : '预警已创建', [
        { text: '确定', onPress: () => navigation.goBack() },
      ]);
    } catch (e: any) {
      Alert.alert('失败', e.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* 品种选择 */}
      <View style={styles.card}>
        <Text style={styles.label}>选择品种</Text>
        <View style={styles.productRow}>
          {products.map((p) => (
            <TouchableOpacity
              key={p.id}
              style={[styles.productBtn, productId === p.id && styles.productBtnActive]}
              onPress={() => setProductId(p.id)}
            >
              <Text style={[styles.productBtnText, productId === p.id && styles.productBtnTextActive]}>
                {p.name}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* 阀值设置 */}
      <View style={styles.card}>
        <Text style={styles.label}>价格阀值</Text>

        <View style={styles.inputRow}>
          <Text style={styles.inputLabel}>最高阀值（元/克）</Text>
          <TextInput
            style={styles.input}
            value={upperLimit}
            onChangeText={setUpperLimit}
            keyboardType="decimal-pad"
            placeholder="不设置则留空"
          />
        </View>

        <View style={styles.divider} />

        <View style={styles.inputRow}>
          <Text style={styles.inputLabel}>最低阀值（元/克）</Text>
          <TextInput
            style={styles.input}
            value={lowerLimit}
            onChangeText={setLowerLimit}
            keyboardType="decimal-pad"
            placeholder="不设置则留空"
          />
        </View>
      </View>

      {/* 启用开关 */}
      <View style={styles.card}>
        <View style={styles.switchRow}>
          <Text style={styles.switchLabel}>启用预警</Text>
          <Switch
            value={warnEnable}
            onValueChange={setWarnEnable}
            trackColor={{ false: '#ddd', true: '#d4a84b' }}
            thumbColor="#fff"
          />
        </View>
      </View>

      {/* 保存 */}
      <TouchableOpacity
        style={[styles.saveBtn, saving && styles.saveBtnDisabled]}
        onPress={handleSave}
        disabled={saving}
      >
        <Text style={styles.saveBtnText}>{saving ? '保存中...' : '保存'}</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  content: { paddingBottom: 40 },
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
  label: { fontSize: 15, fontWeight: '700', color: '#1a1a2e', marginBottom: 10 },
  productRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  productBtn: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  productBtnActive: { backgroundColor: '#d4a84b', borderColor: '#d4a84b' },
  productBtnText: { fontSize: 13, color: '#666' },
  productBtnTextActive: { color: '#fff', fontWeight: '600' },
  inputRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  inputLabel: { fontSize: 14, color: '#333' },
  input: {
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    padding: 8,
    width: 140,
    textAlign: 'right',
    fontSize: 14,
  },
  divider: { height: 1, backgroundColor: '#f0f0f0' },
  switchRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  switchLabel: { fontSize: 15, color: '#333' },
  saveBtn: {
    backgroundColor: '#d4a84b',
    borderRadius: 10,
    padding: 16,
    margin: 16,
    alignItems: 'center',
  },
  saveBtnDisabled: { opacity: 0.6 },
  saveBtnText: { color: '#fff', fontSize: 17, fontWeight: '700' },
});
