package {{PACKAGE_NAME}}

import android.content.Context
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import java.io.ByteArrayInputStream
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest

object OfflineHandler {

    private const val CACHE_DIR = "webview_cache"
    private const val MAX_CACHE_AGE_MS = 24 * 60 * 60 * 1000L // 24 hours

    fun interceptRequest(context: Context?, request: WebResourceRequest?): WebResourceResponse? {
        if (context == null || request == null) return null

        val url = request.url.toString()
        
        if (!shouldCache(url)) {
            return null
        }

        val cacheFile = getCacheFile(context, url)
        
        if (isCacheValid(cacheFile)) {
            return loadFromCache(cacheFile, url)
        }

        return fetchAndCache(context, url, cacheFile)
    }

    private fun shouldCache(url: String): Boolean {
        val cacheable = listOf(
            ".css", ".js", ".jpg", ".jpeg", ".png", ".gif", 
            ".svg", ".woff", ".woff2", ".ttf", ".eot", ".ico"
        )
        return cacheable.any { url.contains(it, ignoreCase = true) }
    }

    private fun getCacheFile(context: Context, url: String): File {
        val cacheDir = File(context.cacheDir, CACHE_DIR)
        if (!cacheDir.exists()) {
            cacheDir.mkdirs()
        }
        
        val filename = generateCacheKey(url)
        return File(cacheDir, filename)
    }

    private fun generateCacheKey(url: String): String {
        return try {
            val digest = MessageDigest.getInstance("MD5")
            val hash = digest.digest(url.toByteArray())
            hash.joinToString("") { "%02x".format(it) }
        } catch (e: Exception) {
            url.hashCode().toString()
        }
    }

    private fun isCacheValid(cacheFile: File): Boolean {
        if (!cacheFile.exists()) return false
        
        val age = System.currentTimeMillis() - cacheFile.lastModified()
        return age < MAX_CACHE_AGE_MS
    }

    private fun loadFromCache(cacheFile: File, url: String): WebResourceResponse? {
        return try {
            val inputStream = FileInputStream(cacheFile)
            val mimeType = getMimeType(url)
            val encoding = "UTF-8"
            WebResourceResponse(mimeType, encoding, inputStream)
        } catch (e: Exception) {
            null
        }
    }

    private fun fetchAndCache(context: Context, url: String, cacheFile: File): WebResourceResponse? {
        return try {
            val connection = URL(url).openConnection() as HttpURLConnection
            connection.connectTimeout = 5000
            connection.readTimeout = 5000
            connection.connect()

            if (connection.responseCode == HttpURLConnection.HTTP_OK) {
                val inputStream = connection.inputStream
                val bytes = inputStream.readBytes()
                inputStream.close()

                FileOutputStream(cacheFile).use { it.write(bytes) }

                val cachedInputStream = ByteArrayInputStream(bytes)
                val mimeType = connection.contentType ?: getMimeType(url)
                val encoding = connection.contentEncoding ?: "UTF-8"
                
                WebResourceResponse(mimeType, encoding, cachedInputStream)
            } else {
                null
            }
        } catch (e: Exception) {
            if (cacheFile.exists()) {
                loadFromCache(cacheFile, url)
            } else {
                null
            }
        }
    }

    private fun getMimeType(url: String): String {
        return when {
            url.endsWith(".css") -> "text/css"
            url.endsWith(".js") -> "application/javascript"
            url.endsWith(".json") -> "application/json"
            url.endsWith(".png") -> "image/png"
            url.endsWith(".jpg") || url.endsWith(".jpeg") -> "image/jpeg"
            url.endsWith(".gif") -> "image/gif"
            url.endsWith(".svg") -> "image/svg+xml"
            url.endsWith(".woff") -> "font/woff"
            url.endsWith(".woff2") -> "font/woff2"
            url.endsWith(".ttf") -> "font/ttf"
            url.endsWith(".eot") -> "application/vnd.ms-fontobject"
            url.endsWith(".ico") -> "image/x-icon"
            else -> "text/plain"
        }
    }

    fun clearCache(context: Context) {
        val cacheDir = File(context.cacheDir, CACHE_DIR)
        if (cacheDir.exists()) {
            cacheDir.deleteRecursively()
        }
    }

    fun getCacheSize(context: Context): Long {
        val cacheDir = File(context.cacheDir, CACHE_DIR)
        if (!cacheDir.exists()) return 0
        
        return cacheDir.walkTopDown().filter { it.isFile }.map { it.length() }.sum()
    }
}
