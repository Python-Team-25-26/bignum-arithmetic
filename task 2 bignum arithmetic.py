class BigNum:

    M = 1000
    N = 100

    def __init__(self, value: int = 0):
        if value > BigNum.M ** BigNum.N:
            raise OverflowError("BigNum Overflow Error")
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
                s = "0" + s
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
        if isinstance(other, int):
            other = BigNum(other)

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
            if len(result.digits) + 1 > BigNum.N:
                raise OverflowError("BigNum Overflow Error")

            result.digits.append(total % self.M)

        return result

    def __sub__(self, other):
        if isinstance(other, int):
            other = BigNum(other)

        if self.sign != other.sign:
            return self + (-other)

        abs_compare = self._compare_abs(other)

        if abs_compare == 0:
            return BigNum(0)

        result = BigNum()

        if abs_compare > 0:  
            result.sign = self.sign
            larger, smaller = self, other
        else: 
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
        if isinstance(other, int):
            other = BigNum(other)

        result = BigNum(0)
        result.digits = [0] * (len(self.digits) + len(other.digits) + 1)

        for i in range(len(self.digits)):
            carry = 0
            for j in range(len(other.digits)):
                product = (
                    self.digits[i] * other.digits[j] + result.digits[i + j] + carry
                )
                carry = product // self.M
                result.digits[i + j] = product % self.M

            if carry > 0:
                result.digits[i + len(other.digits)] += carry

            if len(result.digits) + 1 > BigNum.N:
                raise OverflowError("BigNum Overflow Error")


        while len(result.digits) > 1 and result.digits[-1] == 0:
            result.digits.pop()

        result.sign = self.sign * other.sign
        return result

    def __floordiv__(self, other):
 
     if isinstance(other, int):
        other = BigNum(other)
    
     if other._compare_abs(BigNum(0))==0:
        raise ZeroDivisionError("Division by zero")  
    
     result_sign = self.sign * other.sign
   
     dividend = BigNum()
     dividend.copy(self)
     divisor = BigNum()
     divisor.copy(other)
     dividend.sign = divisor.sign = 1


     if dividend._compare_abs(divisor) < 0:
         return BigNum(0)
    
 
     if dividend._compare_abs(divisor) == 0: 
        result = BigNum(1)  
        result.sign = result_sign
        return result

    
     if divisor._compare_abs(BigNum(1)) == 0:
        result = BigNum()
        result.copy(self)
        result.sign = result_sign
        return result
 
     quotient = BigNum(0)
     remainder = BigNum(0)
   
     for i in range(len(dividend.digits) - 1, -1, -1):
        remainder = remainder * BigNum(self.M) + BigNum(dividend.digits[i])
        
        if remainder._compare_abs(divisor) < 0:
            quotient = quotient * BigNum(self.M)
            continue
        
        
        digit = 0
        for j in range(1, self.M):  
            temp_product = divisor * BigNum(j)
            
            if temp_product._compare_abs(remainder) <= 0:
                digit = j  
            else:
                break 
       
        quotient = quotient * BigNum(self.M) + BigNum(digit)
        
  
        remainder = remainder - divisor * BigNum(digit)
    
    
     quotient.sign = result_sign
     return quotient


          


if __name__ == "__main__":
    A = BigNum(123456)
    B = BigNum(789012)
    print(A, B, A+B)

    C = BigNum(-999)
    D = BigNum(-1000)
    print(C, D, C-D)

    E = BigNum(-123)
    F = BigNum(456)
    print(E, F, E*F)

    G = BigNum(-123456)
    H = BigNum(-123)
    print(G, H, G//H)



