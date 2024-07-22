from evennia import CmdSet
from evennia import default_cmds
from evennia.commands.default import general

# from evennia.commands.default.general import \
#     CmdHome as Home, \
#     CmdLook as Look, \
#     CmdNick as Nick, \
#     CmdInventory as Inventory, \
#     CmdSetDesc as SetDesc, \
#     CmdGet as Get, \
#     CmdDrop as Drop, \
#     CmdGive as Give, \
#     CmdSay as Say, \
#     CmdWhisper as Whisper, \
#     CmdPose as Pose, \
#     CmdAccess as Access

from commands.command import Command


##############################################
# Custom Base Class
##############################################

class CustomBaseCmd(Command):
    """
    A custom base class to override Evennia's default commands.
    """

    def at_post_cmd(self):
        """
        Retrieves caller's (character's) resources values and displays them in a prompt after each command has been
        executed.
        """
        caller = self.caller
        hp = f"{caller.db.current_hp}/{caller.db.max_hp}"
        mana = f"{caller.db.current_mana}/{caller.db.max_mana}"
        stam = f"{caller.db.current_stam}/{caller.db.max_stam}"
        prompt = f"\n|r HP({hp}) |m Mana({mana}) |g Stamina({stam})|n\n"
        print("Prompt:", prompt)  # Add this line to print the generated prompt
        caller.msg(prompt=prompt)


##############################################
# Character Cmd overrides
##############################################

class CmdLook(general.CmdLook, CustomBaseCmd):

    aliases = ["l", "loo", "lo"]

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdHome(general.CmdHome, CustomBaseCmd):

    key = "recall"
    aliases = ["home", "rec"]

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdInventory(default_cmds.CmdInventory, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdSetDesc(default_cmds.CmdSetDesc, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdGet(default_cmds.CmdGet, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdDrop(default_cmds.CmdDrop, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdGive(default_cmds.CmdGive, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdSay(default_cmds.CmdSay, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdWhisper(default_cmds.CmdWhisper, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdPose(default_cmds.CmdPose, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdAccess(default_cmds.CmdAccess, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


class CmdNick(default_cmds.CmdNick, CustomBaseCmd):

    def at_post_cmd(self):
        # A direct call to the CustomBaseCmd at_post_cmd method / super().at_post_cmd() fails to invoke it.
        CustomBaseCmd.at_post_cmd(self)


##############################################
# Account Cmd overrides
##############################################


##############################################
# My custom commands
##############################################

class StatSheet(CustomBaseCmd):
    """
    Shows player attributes by displaying the stat-sheet.

    Usage:
    score or sc
    """
    key = "stat"
    aliases = ["stats", "ss"]

    def parse(self):
        # Strip the arguments to remove and leading/trailing whitespace
        self.args = self.args.strip()

        # Check if the command matches score or sc
        if self.args in self.aliases:
            self.args = ""

    def func(self):
        # Retrieve the stat_sheet from the callers object
        stat_sheet = self.caller.db.stat_sheet

        if stat_sheet:
            # If stat_sheet is not empty or None, send it to the player
            self.caller.msg(stat_sheet)
        else:
            # if the stat_sheet is empty or None, send an error message to the player
            self.caller.msg("The stat sheet is not available.")


##############################################
# My custom command sets
##############################################

class MyCmdSet(CmdSet):
    """
    Adds MyCmdSet to default_cmdsets.py in the SessionCmdSet class
    """

    def at_cmdset_creation(self):
        # Evennia's stock commands
        self.add(StatSheet)
