#!/bin/bash
# SacredSpace OS — Configure Rclone Cloudflare R2
# Requires: R2 Access Key ID, Secret Access Key
# Run once after creating R2 bucket

SACRED_ROOT="/mnt/d/SacredSpace_OS"
echo "⟡ SacredSpace OS — Rclone R2 Configuration"
echo ""
echo "You need:"
echo "  1. Cloudflare R2 bucket (create at https://dash.cloudflare.com/)"
echo "  2. R2 Access Key ID"
echo "  3. R2 Secret Access Key"
echo ""

read -p "R2 Access Key ID: " r2_key
read -sp "R2 Secret Access Key: " r2_secret
echo ""
read -p "R2 Bucket Name [sacredspace-backup]: " r2_bucket
r2_bucket=${r2_bucket:-sacredspace-backup}
read -p "R2 Endpoint URL [https://<accountid>.r2.cloudflarestorage.com]: " r2_endpoint

rclone config create sacredspace_r2 s3 \
    provider Cloudflare \
    access_key_id "$r2_key" \
    secret_access_key "$r2_secret" \
    region auto \
    endpoint "$r2_endpoint" \
    acl private

echo ""
echo "✓ R2 remote 'sacredspace_r2' configured"
echo ""
echo "To test: rclone ls sacredspace_r2:$r2_bucket"
echo "To sync: rclone sync $SACRED_ROOT sacredspace_r2:$r2_bucket --progress --encrypted"
