class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        # 如果输入是空列表，直接返回空字符串
        if not strs:
            return ""

        # 假设第一个字符串是前缀
        prefix = strs[0]

        # 遍历剩下的每一个字符串
        for s in strs[1:]:
            # 如果当前字符串 s 不是以 prefix 开头
            while not s.startswith(prefix):
                # 去掉 prefix 最后一个字符
                prefix = prefix[:-1]
                # 如果前缀被删空，说明没有公共前缀
                if not prefix:
                    return ""
        # 返回最后的公共前缀
        return prefix
