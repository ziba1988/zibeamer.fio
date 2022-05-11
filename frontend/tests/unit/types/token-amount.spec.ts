import { TokenAmount } from '@/types/token-amount';
import {
  generateToken,
  generateTokenAmountData,
  generateUInt256Data,
} from '~/utils/data_generators';

describe('TokenAmount', () => {
  describe('parse()', () => {
    it('can parse integer based on given token decimals', () => {
      const token = generateToken({ decimals: 5 });
      const amount = TokenAmount.parse('12345', token);

      expect(amount.decimalAmount).toBe('12345.0');
    });

    it('has no final zero after period if decimals are zero', () => {
      const token = generateToken({ decimals: 0 });
      const amount = TokenAmount.parse('12345', token);

      expect(amount.decimalAmount).toBe('12345');
    });

    it('can parse floating number bases on givevn decimals', () => {
      const token = generateToken({ decimals: 18 });
      const amount = TokenAmount.parse('12.345', token);

      expect(amount.decimalAmount).toBe('12.345');
    });
  });

  describe('uint256', () => {
    it('allows to access amount as UInt256 for blockchain interactions', () => {
      const token = generateToken();
      const amount = new TokenAmount({ amount: '100', token });

      expect(amount.uint256).toBeDefined();
      expect(amount.uint256.asString).toBe('100');
    });
  });

  describe('formattedAmount', () => {
    it('returns the decimals value plus the token symbol', () => {
      const token = generateToken({ decimals: 2, symbol: 'TTT' });
      const amount = new TokenAmount({ amount: '100', token });

      expect(amount.formattedAmount).toBe('1.0 TTT');
    });
  });

  describe('encode()', () => {
    it('serializes all data to persist token amount', () => {
      const token = generateToken();
      const amount = generateUInt256Data();
      const data = { amount, token };
      const tokenAmount = new TokenAmount(data);

      const encodedData = tokenAmount.encode();

      expect(encodedData.amount).toMatchObject(amount);
      expect(encodedData.token).toMatchObject(token);
    });

    it('can be used to re-instantiate token amount again', () => {
      const data = generateTokenAmountData();
      const amount = new TokenAmount(data);

      const encodedData = amount.encode();
      const newTokenAmount = new TokenAmount(encodedData);
      const newEncodedData = newTokenAmount.encode();

      expect(encodedData).toMatchObject(newEncodedData);
    });
  });
});