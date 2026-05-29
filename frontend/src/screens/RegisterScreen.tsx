import React, { useState } from 'react';
import {
  Alert, KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text,
  TextInput, TouchableOpacity, View,
} from 'react-native';
import { useAuth } from '../store/AuthContext';

export default function RegisterScreen({ navigation }: any) {
  const { register } = useAuth();
  const [phone, setPhone] = useState('');
  const [code, setCode] = useState('');
  const [agreed, setAgreed] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (!phone || !code) {
      Alert.alert('提示', '请填写手机号和验证码');
      return;
    }
    if (!agreed) {
      Alert.alert('提示', '请先同意用户使用协议和隐私政策');
      return;
    }
    setLoading(true);
    try {
      await register(phone, code, true);
    } catch (e: any) {
      Alert.alert('注册失败', e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>用户注册</Text>

        <View style={styles.form}>
          <Text style={styles.label}>手机号</Text>
          <TextInput
            style={styles.input}
            placeholder="请输入手机号"
            keyboardType="phone-pad"
            maxLength={15}
            value={phone}
            onChangeText={setPhone}
          />

          <Text style={styles.label}>验证码</Text>
          <TextInput
            style={styles.input}
            placeholder="请输入验证码"
            keyboardType="number-pad"
            maxLength={6}
            value={code}
            onChangeText={setCode}
          />

          <TouchableOpacity
            style={styles.agreement}
            onPress={() => setAgreed(!agreed)}
          >
            <View style={[styles.checkbox, agreed && styles.checkboxActive]}>
              {agreed && <Text style={styles.checkmark}>✓</Text>}
            </View>
            <Text style={styles.agreementText}>
              我已阅读并同意
              <Text style={styles.link} onPress={() => Alert.alert('用户使用协议', '这是用户使用协议内容...')}> 用户使用协议 </Text>
              和
              <Text style={styles.link} onPress={() => Alert.alert('隐私政策', '这是隐私政策内容...')}> 隐私政策</Text>
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.submitBtn, loading && styles.submitBtnDisabled]}
            onPress={handleRegister}
            disabled={loading}
          >
            <Text style={styles.submitText}>{loading ? '注册中...' : '注册'}</Text>
          </TouchableOpacity>

          <TouchableOpacity onPress={() => navigation.goBack()}>
            <Text style={styles.link}>已有账号？去登录</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  scroll: { flexGrow: 1, padding: 24, justifyContent: 'center' },
  title: { fontSize: 28, fontWeight: '800', color: '#1a1a2e', textAlign: 'center', marginBottom: 24 },
  form: { backgroundColor: '#fff', borderRadius: 16, padding: 24, shadowColor: '#000', shadowOpacity: 0.06, shadowRadius: 12, elevation: 3 },
  label: { fontSize: 14, fontWeight: '600', color: '#333', marginBottom: 6, marginTop: 12 },
  input: { borderWidth: 1, borderColor: '#e0e0e0', borderRadius: 10, padding: 14, fontSize: 16, backgroundColor: '#fafafa' },
  agreement: { flexDirection: 'row', alignItems: 'center', marginTop: 16, gap: 8 },
  checkbox: { width: 22, height: 22, borderRadius: 4, borderWidth: 2, borderColor: '#ccc', justifyContent: 'center', alignItems: 'center' },
  checkboxActive: { backgroundColor: '#d4a84b', borderColor: '#d4a84b' },
  checkmark: { color: '#fff', fontSize: 14, fontWeight: '700' },
  agreementText: { fontSize: 13, color: '#666', flex: 1 },
  link: { color: '#d4a84b', fontWeight: '600' },
  submitBtn: { backgroundColor: '#d4a84b', borderRadius: 10, padding: 16, alignItems: 'center', marginTop: 20 },
  submitBtnDisabled: { opacity: 0.6 },
  submitText: { color: '#fff', fontSize: 18, fontWeight: '700' },
});
