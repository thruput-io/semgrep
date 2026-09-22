# ruleid: scripts-abort-on-error
rm -rf "$TARGET_DIR"
cp important.conf /etc/app/important.conf
systemctl restart app
