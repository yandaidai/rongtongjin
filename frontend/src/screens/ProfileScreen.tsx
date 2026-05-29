import React, { useState } from 'react';
import {
  Alert, ScrollView, StyleSheet, Text, TextInput, TouchableOpacity, View,
} from 'react-native';
import { api } from '../api/client';
import { useAuth } from '../store/AuthContext';

export default function ProfileScreen({ navigation }: any) {
  const { user, logout, refreshUser } = useAuth();
  const [nickname, setNickname] = useState(user?.nickname || '');
  const [password, setPassword] = useState('');
  const [editingNickname, setEditingNickname] = useState(false);
  const [editingPassword, setEditingPassword] = useState(false);

  const handleUpdateNickname = async () => {
    if (!nickname.trim()) return;
    try {
      await api.updateNickname(nickname.trim());
      await refreshUser();
      setEditingNickname(false);
      Alert.alert('成功', '昵称已更新');
    } catch (e: any) {
      Alert.alert('失败', e.message);
    }
  };

  const handleSetPassword = async () => {
    if (password.length < 6) {
      Alert.alert('提示', '密码至少6位');
      return;
    }
    try {
      await api.setPassword(password);
      setEditingPassword(false);
      setPassword('');
      Alert.alert('成功', '密码已设置');
    } catch (e: any) {
      Alert.alert('失败', e.message);
    }
  };

  const handleDeactivate = () => {
    Alert.alert(
      '确认注销',
      '注销后账号将被停用，是否继续？',
      [
        { text: '取消', style: 'cancel' },
        {
          text: '确认注销',
          style: 'destructive',
          onPress: async () => {
            try {
              await api.deactivateAccount();
              await logout();
            } catch (e: any) {
              Alert.alert('失败', e.message);
            }
          },
        },
      ],
    );
  };

  const handleLogout = () => {
    Alert.alert('退出登录', '确定退出当前账号？', [
      { text: '取消', style: 'cancel' },
      { text: '退出', onPress: () => logout() },
    ]);
  };

  return (
    <ScrollView style={styles.container}>
      {/* 用户信息卡片 */}
      <View style={styles.card}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {user?.nickname?.charAt(0) || user?.phone?.charAt(0) || '?'}
          </Text>
        </View>
        <Text style={styles.nickname}>{user?.nickname || '未设置昵称'}</Text>
        <Text style={styles.phone}>手机号: {user?.phone}</Text>
        <Text style={styles.userId}>ID: {user?.id}</Text>
      </View>

      {/* 昵称设置 */}
      <View style={styles.card}>
        <Text style={styles.sectionTitle}>基本资料</Text>

        {editingNickname ? (
          <View style={styles.editRow}>
            <TextInput
              style={styles.input}
              value={nickname}
              onChangeText={setNickname}
              placeholder="输入新昵称"
            />
            <TouchableOpacity style={styles.saveBtn} onPress={handleUpdateNickname}>
              <Text style={styles.saveBtnText}>保存</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setEditingNickname(false)}>
              <Text style={styles.cancelText}>取消</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity style={styles.menuItem} onPress={() => setEditingNickname(true)}>
            <Text style={styles.menuLabel}>修改昵称</Text>
            <Text style={styles.menuArrow}>›</Text>
          </TouchableOpacity>
        )}

        <View style={styles.divider} />

        {/* 点差配置 */}
        <TouchableOpacity
          style={styles.menuItem}
          onPress={() => navigation.navigate('SpreadConfig')}
        >
          <Text style={styles.menuLabel}>点差配置</Text>
          <Text style={styles.menuArrow}>›</Text>
        </TouchableOpacity>

        <View style={styles.divider} />

        {/* 预警配置 */}
        <TouchableOpacity
          style={styles.menuItem}
          onPress={() => navigation.navigate('WarnList')}
        >
          <Text style={styles.menuLabel}>价格预警</Text>
          <Text style={styles.menuArrow}>›</Text>
        </TouchableOpacity>
      </View>

      {/* 密码设置 */}
      <View style={styles.card}>
        <Text style={styles.sectionTitle}>安全设置</Text>

        {editingPassword ? (
          <View style={styles.editRow}>
            <TextInput
              style={[styles.input, { flex: 1 }]}
              value={password}
              onChangeText={setPassword}
              placeholder="输入新密码（至少6位）"
              secureTextEntry
            />
            <TouchableOpacity style={styles.saveBtn} onPress={handleSetPassword}>
              <Text style={styles.saveBtnText}>设置</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setEditingPassword(false)}>
              <Text style={styles.cancelText}>取消</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <TouchableOpacity style={styles.menuItem} onPress={() => setEditingPassword(true)}>
            <Text style={styles.menuLabel}>设置密码</Text>
            <Text style={styles.menuArrow}>›</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* 操作按钮 */}
      <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
        <Text style={styles.logoutText}>退出登录</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.deactivateBtn} onPress={handleDeactivate}>
        <Text style={styles.deactivateText}>注销账号</Text>
      </TouchableOpacity>

      <View style={{ height: 40 }} />
    </ScrollView>
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
    shadowRadius: 8,
    elevation: 2,
  },
  avatar: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: '#d4a84b',
    justifyContent: 'center',
    alignItems: 'center',
    alignSelf: 'center',
    marginBottom: 8,
  },
  avatarText: { fontSize: 28, fontWeight: '700', color: '#fff' },
  nickname: { fontSize: 18, fontWeight: '700', color: '#1a1a2e', textAlign: 'center' },
  phone: { fontSize: 14, color: '#666', textAlign: 'center', marginTop: 4 },
  userId: { fontSize: 12, color: '#999', textAlign: 'center', marginTop: 2 },
  sectionTitle: { fontSize: 15, fontWeight: '700', color: '#1a1a2e', marginBottom: 10 },
  editRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  input: {
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    padding: 10,
    fontSize: 14,
    flex: 1,
  },
  saveBtn: { backgroundColor: '#d4a84b', borderRadius: 8, paddingHorizontal: 16, paddingVertical: 10 },
  saveBtnText: { color: '#fff', fontWeight: '600' },
  cancelText: { color: '#999', fontSize: 14 },
  menuItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
  },
  menuLabel: { fontSize: 15, color: '#333' },
  menuArrow: { fontSize: 20, color: '#ccc' },
  divider: { height: 1, backgroundColor: '#f0f0f0' },
  logoutBtn: {
    backgroundColor: '#fff',
    borderRadius: 12,
    margin: 16,
    marginBottom: 0,
    padding: 16,
    alignItems: 'center',
  },
  logoutText: { color: '#e74c3c', fontSize: 16, fontWeight: '600' },
  deactivateBtn: { margin: 16, alignItems: 'center' },
  deactivateText: { color: '#999', fontSize: 14 },
});
