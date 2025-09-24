class BigNum:

    M = 10
    N = 100

    def __init__(self, value: int = 0):
        self.sign = 1
        self.digits = []
        if value != 0:
            self._from_int(value)

    def copy(self, other):
        self.digits = other.digits.copy()
        self.sign = other.sign

    def _from_int(self, n: int):
        if n == 0:
            self.digits = [0]
            self.sign = 1
            return
            
        self.sign = 1 if n >= 0 else -1
        n = abs(n)
        
        self.digits = []
        while n > 0:
            self.digits.append(n % self.M)
            n //= self.M
            
        if not self.digits:
            self.digits = [0]

    def __str__(self):
        if not self.digits:
            return "0"
            
        digit_strs = []
        for digit in self.digits:
            s = str(digit)
            while len(s) < len(str(self.M - 1)):
                s = '0' + s
            digit_strs.append(s)

        result = ".".join(reversed(digit_strs))

        if self.sign == -1:
            result = "-" + result
            
        return result
    
    def __neg__(self):
        result = BigNum()
        result.copy(self)
        result.sign *= -1
        return result
    
    def __add__(self, other):

        if self.sign != other.sign:
            if self.sign == -1:
                return other - (-self)
            else:
                return self - (-other)

        result = BigNum()
        result.sign = self.sign

        carry = 0
        max_len = max(len(self.digits), len(other.digits))
        result.digits = []

        for i in range(max_len):
            a = self.digits[i] if i < len(self.digits) else 0
            b = other.digits[i] if i < len(other.digits) else 0
            
            total = a + b + carry
            carry = total // self.M
            result.digits.append(total % self.M)

        return result
    
    def __sub__(self, other):
        
        if self.sign != other.sign:
            return self + (-other)
        
        abs_compare = self._compare_abs(other)
        
        if abs_compare == 0:
            return BigNum(0)
        
        result = BigNum()
        
        if abs_compare > 0:  # self > other
            result.sign = self.sign
            larger, smaller = self, other
        else:  # self < other
            result.sign = -self.sign
            larger, smaller = other, self
        
        borrow = 0
        for i in range(len(larger.digits)):
            a = larger.digits[i]
            b = smaller.digits[i] if i < len(smaller.digits) else 0
            
            diff = a - b - borrow
            if diff < 0:
                diff += self.M
                borrow = 1
            else:
                borrow = 0
            
            result.digits.append(diff)
        
        while len(result.digits) > 1 and result.digits[-1] == 0:
            result.digits.pop()

        return result
    
    def _compare_abs(self, other) -> int:
        if len(self.digits) > len(other.digits):
            return 1
        elif len(self.digits) < len(other.digits):
            return -1
        
        for i in range(len(self.digits) - 1, -1, -1):
            if self.digits[i] > other.digits[i]:
                return 1
            elif self.digits[i] < other.digits[i]:
                return -1
        return 0
            
    def __mul__(self, other):
        result = BigNum(0)
        result.digits = [0] * (len(self.digits) + len(other.digits) + 1)
        
        for i in range(len(self.digits)):
            carry = 0
            for j in range(len(other.digits)):
                product = self.digits[i] * other.digits[j] + result.digits[i + j] + carry
                carry = product // self.M
                result.digits[i + j] = product % self.M
                
            if carry > 0:
                result.digits[i + len(other.digits)] += carry
                
        while len(result.digits) > 1 and result.digits[-1] == 0:
            result.digits.pop()
        
        result.sign = self.sign * other.sign
        return result
    
    def __floordiv__(self, other):
        
        result_sign = self.sign * other.sign
        
        dividend = BigNum()
        dividend.copy(self)
        divisor = BigNum()
        divisor.copy(other)
        dividend.sign = divisor.sign = 1
        
        # Если делимое меньше делителя
        if dividend._compare_abs(divisor) < 0:
            return BigNum(0)
        
        if divisor == BigNum(1):
            result = BigNum()
            result.copy(self)
            result.sign = result_sign
            return result
        
        quotient = 0
        while dividend._compare_abs(divisor) >= 0:
            dividend -= divisor
            quotient += 1

        return BigNum(quotient)
if __name__ == "__main__":
    A = BigNum(12)
    B = A * A
    print(A, B, A * BigNum(9))
    print(B // A)
    print((BigNum(15) // BigNum(2)) * BigNum(2))