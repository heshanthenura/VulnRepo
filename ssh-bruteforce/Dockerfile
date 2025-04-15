# Use Ubuntu as the base image
FROM ubuntu:20.04

# Set non-interactive mode to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install OpenSSH server
RUN apt-get update && \
    apt-get install -y openssh-server && \
    apt-get clean && \
    # Set the root password to a weak one (toor)
    echo "root:toor" | chpasswd && \
    # Allow root to login via SSH
    sed -i 's/^#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    # Allow password-based authentication
    sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    # Create the directory for SSH server
    mkdir /var/run/sshd

# Expose the SSH port (22)
EXPOSE 22

# Start the SSH service in the foreground
CMD ["/usr/sbin/sshd", "-D"]
